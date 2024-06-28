import axios from "axios";
import React, { useState } from "react";
import { useCookies } from "react-cookie";
import { Button, Card, Form, InputGroup, ListGroup, OverlayTrigger, Tooltip } from "react-bootstrap";
import { BsSearch, BsRobot, BsCardText } from "react-icons/bs";

export default function IndexSearch({ selectedFile }) {
    const [cookies] = useCookies(['token']);
    const [query, setQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [botResponse, setBotResponse] = useState('');

    const handleQuery = async (query) => {
        try {
            const token = cookies.token;
            const object_name = selectedFile.name.split(".")[0];
            console.log("Sending query:", query, "to object:", object_name);
            console.log("Token:", token);
            const response = await axios.get("http://localhost:8000/document-search", {
                params: { query, object_name }
            });
            setBotResponse(response.data.data.llm_response);
            setSearchResults(response.data.data.search_results || []);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await handleQuery(query);
    };

    return (
        <>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <InputGroup>
                        <Form.Control
                            type="text"
                            placeholder="Query"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <OverlayTrigger
                            key={"top"}
                            placement={"top"}
                            overlay={
                                <Tooltip id={`tooltip-top`}>
                                    Send search query
                                </Tooltip>
                            }
                        >
                            <Button variant="outline-secondary" id="button-addon2" type="submit">
                                <BsSearch />
                            </Button>
                        </OverlayTrigger>
                    </InputGroup>
                </Form.Group>
            </Form>
            <hr />
            <Card style={{ height: "20vh", maxHeight: "20vh" }}>
                <Card.Header>
                    <Card.Title className="d-flex align-items-center">
                        <BsRobot className="me-2" />
                        Bot Response
                    </Card.Title>
                </Card.Header>
                <Card.Body className="overflow-y-auto">
                    <p>{botResponse}</p>
                </Card.Body>
            </Card>
            <Card className="mt-3" style={{ height: "48vh", maxHeight: "48vh" }}>
                <Card.Header>
                    <Card.Title className="d-flex align-items-center">
                        <BsCardText className="me-2" />
                        Document Parts Found
                    </Card.Title>
                </Card.Header>
                <Card.Body>
                    <ListGroup className="overflow-y-auto" style={{ maxHeight: "38vh" }}>
                        {searchResults.map((result, index) => (
                            <ListGroup.Item key={index} className="overflow-y-auto my-1 shadow-sm" style={{ maxHeight: "10vh", height: "10vh" }}>
                                <div className="d-flex justify-content-between">
                                    <div className="d-flex">
                                        <span>{result.page_content}</span>
                                    </div>
                                    <div>
                                        <span>{index + 1}</span>
                                    </div>
                                </div>
                            </ListGroup.Item>
                        ))}
                    </ListGroup>
                </Card.Body>
            </Card>
        </>
    );
}
