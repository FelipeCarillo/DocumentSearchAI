import { Card, Form } from "react-bootstrap";

export default function Query() {
    return (
        <Card className='m-3 h-100'>
            <Card.Body>
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Label>Query</Form.Label>
                        <Form.Control type="text" placeholder="Enter query" />
                    </Form.Group>
                </Form>
            </Card.Body>
        </Card>
    );
}