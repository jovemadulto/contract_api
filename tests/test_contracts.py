import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.models import Contract
from sqlalchemy.orm import Session
import json
import io

# --- /contracts/upload Tests ---

def test_upload_unauthenticated(client: TestClient):
    """
    Tests that the /upload endpoint is protected and returns 401
    if no authentication token is provided.
    """
    file_content = b"fake pdf content"
    file = ("contract.pdf", io.BytesIO(file_content), "application/pdf")
    
    response = client.post(
        "/contracts/upload",
        files={"file": file}
    )
    # The dependency get_current_user will raise 401
    assert response.status_code == 401

def test_upload_invalid_file_type(authenticated_client: TestClient):
    """
    Tests that uploading a file with an invalid extension (e.g., .txt)
    is correctly rejected with a 400 error.
    """
    file_content = b"this is a plain text file"
    file = ("test.txt", io.BytesIO(file_content), "text/plain")
    
    response = authenticated_client.post(
        "/contracts/upload",
        files={"file": file}
    )
    assert response.status_code == 400
    assert "Formato de arquivo inválido" in response.json()["detail"]

@patch("app.contracts.extract_contract_info")
@patch("app.contracts.extract_text_from_file")
def test_upload_pdf_success(
    mock_extract_text: MagicMock,
    mock_extract_info: MagicMock,
    authenticated_client: TestClient,
    db_session: Session,
    mock_ai_service_response: dict
):
    """
    Tests the complete successful upload flow for a PDF file.
    - Mocks the text extraction
    - Mocks the AI service call
    - Verifies the API response
    - Verifies the data was saved to the in-memory database
    """
    # 1. Configure Mocks
    mock_extract_text.return_value = "Este é o texto extraído do contrato."
    mock_extract_info.return_value = mock_ai_service_response

    # 2. Prepare Fake File
    file_content = b"fake pdf content" # Content doesn't matter, extraction is mocked
    file = ("contract.pdf", io.BytesIO(file_content), "application/pdf")

    # 3. Make the API Request
    response = authenticated_client.post(
        "/contracts/upload",
        files={"file": file}
    )

    # 4. Check API Response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["filename"] == "contract.pdf"
    assert json_response["contratante"] == mock_ai_service_response["contratante"]
    assert json_response["valor_bens"] == mock_ai_service_response["valor_bens"]

    # 5. Check Mock Calls
    mock_extract_text.assert_called_once()
    mock_extract_info.assert_called_once_with("Este é o texto extraído do contrato.")

    # 6. Check Database
    contract_in_db = db_session.query(Contract).filter(Contract.filename == "contract.pdf").first()
    assert contract_in_db is not None
    assert contract_in_db.contratante == mock_ai_service_response["contratante"]
    assert contract_in_db.vigencia == mock_ai_service_response["vigencia"]


# --- /contracts/{filename} Tests ---

def test_get_contract_unauthenticated(client: TestClient):
    """
    Tests that the GET endpoint is also protected.
    """
    response = client.get("/contracts/test.pdf")
    assert response.status_code == 401

def test_get_contract_not_found(authenticated_client: TestClient):
    """
    Tests getting a 404 response when requesting a contract
    that does not exist in the database.
    """
    response = authenticated_client.get("/contracts/nonexistent.pdf")
    assert response.status_code == 404
    assert response.json() == {"detail": "Contrato não encontrado"}

def test_get_contract_success(
    authenticated_client: TestClient, 
    db_session: Session, 
    mock_ai_service_response: dict
):
    """
    Tests successfully retrieving a contract that exists in the database.
    """
    # 1. Add a contract to the DB first
    new_contract = Contract(
        filename="my_test_contract.pdf",
        **mock_ai_service_response
    )
    db_session.add(new_contract)
    db_session.commit()
    db_session.refresh(new_contract)

    # 2. Try to retrieve it via the API
    response = authenticated_client.get("/contracts/my_test_contract.pdf")

    # 3. Check API Response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == new_contract.id
    assert json_response["filename"] == "my_test_contract.pdf"
    assert json_response["objeto"] == mock_ai_service_response["objeto"]