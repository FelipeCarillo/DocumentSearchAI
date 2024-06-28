import axios from "axios";
import { useEffect, useState } from "react";
import FileList from "../components/FileList";
import FileViewer from "../components/FileViewer";
import IndexSearch from "../components/IndexSearch";
import { Col, Container, Row, Card, Button } from "react-bootstrap";

export default function FileManage() {
    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);

    useEffect(() => {
        if (selectedFile === null) {
            const fetchData = async () => {
                try {
                    console.log(process.env.REACT_APP_API_URL + "/list-files")
                    const response = await axios.get(process.env.REACT_APP_API_URL + "/list-files");
                    setFiles(response.data.data || []);
                } catch (error) {
                    console.log("Error: ", error);
                }
            };
            fetchData();
        }
    }, [selectedFile]);

    return (
        <div className="h-100 p-3">
            <Container fluid >
                <Row md={"12"} style={{ maxHeight: "90vh", height: "90vh" }}>
                    <Col>
                        <Card style={{ maxHeight: '90vh', height: "90vh" }}>
                            <Card.Body>
                                {selectedFile ?
                                    <IndexSearch selectedFile={selectedFile} />
                                    :
                                    <FileList files={files} setSelectedFile={setSelectedFile} />
                                }
                            </Card.Body>
                            {selectedFile &&
                                <Card.Footer>
                                    <Button onClick={() => setSelectedFile(null)}>Back</Button>
                                </Card.Footer>
                            }
                        </Card>
                    </Col>
                    <Col>
                        <FileViewer file={selectedFile} />
                    </Col>
                </Row>
            </Container>
        </div>
    );
}