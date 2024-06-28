import { Card } from "react-bootstrap";

export default function FileViewer({ file }) {
    return (
        <Card className="h-100" style={{ maxHeight: '90vh', height: '90vh' }}>
            <Card.Body>
                <Card.Title>
                    {file ?
                        <div>
                            <strong>{file.name}</strong>
                            <span className="text-muted"> ({file.type})</span>
                        </div>
                        :
                        "No file selected."}
                </Card.Title>
                {file ?
                    <iframe src={file.url} title={file.name} className="w-100 h-100 pb-4" />
                    :
                    <></>
                }
            </Card.Body>
        </Card>
    );
}
