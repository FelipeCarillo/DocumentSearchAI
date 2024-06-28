import React from 'react';
import * as icons from 'react-icons/bs';
import { Button, Navbar } from 'react-bootstrap';

export default function NavBar({ setShow }) {
    return (
        <Navbar bg="dark" variant="dark">
            <Navbar.Brand href="/" className='ms-3'>
                DocumentSearchAI
            </Navbar.Brand>
            <Navbar.Collapse className="justify-content-end me-3">
                <Button variant="outline-light" className='d-flex align-items-center' onClick={() => setShow(true)}>
                    <div className='me-2'>
                        Upload File
                    </div>
                    <icons.BsUpload />
                </Button>
            </Navbar.Collapse>
        </Navbar>
    )
}