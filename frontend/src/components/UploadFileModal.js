import axios from 'axios';
import React, { useState } from 'react';
import { Button, Modal, Form, ProgressBar, Alert } from 'react-bootstrap';

export default function UploadFileModal({ show, setShow }) {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [error, setError] = useState(null);

    const handleClose = () => setShow(false);

    const handleFileToBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    }

    const handleUpload = async () => {
        setUploading(true);
        setError(null);

        try {
            const file_body = await handleFileToBase64(file);
            const body = {
                file_name: file.name,
                file_body: file_body,
                content_type: file.type
            };

            console.log('Uploading file:', body);
            await axios.post(
                'http://localhost:8000/upload-file',
                body
            );

            setFile(null);
            setUploading(false);
            setUploadProgress(0);
            handleClose();
            window.location.reload();
        } catch (err) {
            console.error('Error uploading file:', err);
            setError('Error uploading file. Please try again.');
            setUploading(false);
        }
    }

    return (
        <Modal show={show} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Upload File</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {error && <Alert variant="danger">{error}</Alert>}
                <Form>
                    <Form.Group controlId="formFile" className="mb-3">
                        <Form.Label>Choose a file</Form.Label>
                        <Form.Control type="file" onChange={e => setFile(e.target.files[0])} />
                    </Form.Group>
                    {uploading && <ProgressBar now={uploadProgress} label={`${uploadProgress}%`} />}
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose} disabled={uploading}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleUpload} disabled={!file || uploading}>
                    {uploading ? 'Uploading...' : 'Upload'}
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
