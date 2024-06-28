import { useState, useEffect, useCallback } from 'react';
import * as icons from 'react-icons/bs';
import Badge from 'react-bootstrap/Badge';
import axios from 'axios';
import ListGroup from 'react-bootstrap/ListGroup';
import { Form, InputGroup } from 'react-bootstrap';

export default function FileList({ files = [], setSelectedFile }) {
    const [fileSearch, setFileSearch] = useState('');
    const [filteredFiles, setFilteredFiles] = useState(files || []);

    useEffect(() => {
        if (files.length === 0 || fileSearch === '' || files === undefined || files === null) {
            setFilteredFiles(files);
            return;
        }
        if (fileSearch !== '' && files && files.length > 0) {
            const search = fileSearch.toLowerCase();
            const filtered = files.filter(file => file.name.toLowerCase().includes(search));
            setFilteredFiles(filtered);
        }
    }, [fileSearch, files]);

    const handleDelete = async (file) => {
        await axios.delete(process.env.REACT_APP_API_URL + '/delete-file',
            { params: { file_name: file.name } }
        );
        setSelectedFile(null);
        window.location.reload();
    }

    const handleIcon = useCallback((type) => {
        switch (type) {
            case 'pdf': return <icons.BsFilePdf />;
            case 'doc':
            case 'docx': return <icons.BsFileWord />;
            case 'txt':
            case 'log': return <icons.BsFileText />;
            case 'xls':
            case 'xlsx': return <icons.BsFileExcel />;
            case 'ppt':
            case 'pptx': return <icons.BsFilePpt />;
            case 'zip':
            case 'rar':
            case '7z': return <icons.BsFileZip />;
            case 'jpg':
            case 'jpeg':
            case 'png':
            case 'gif': return <icons.BsFileEarmarkImage />;
            case 'mp3': return <icons.BsFileEarmarkMusic />;
            case 'mp4': return <icons.BsFileEarmarkPlay />;
            case 'exe': return <icons.BsFileEarmarkBinary />;
            default: return <icons.BsFileEarmark />;
        }
    }, []);

    const handleDatetime = useCallback((datetime) => {
        const date = new Date(datetime);
        return date.toLocaleString();
    }, []);

    if (files.length === 0) {
        return <div>No files available.</div>;
    }

    return (
        <>
            <ListGroup>
                <Form>
                    <Form.Group className="mb-3">
                        <InputGroup>
                            <Form.Control
                                type="text"
                                placeholder="Search files"
                                value={fileSearch}
                                onChange={(e) => setFileSearch(e.target.value)}
                            />
                            <InputGroup.Text><icons.BsSearch /></InputGroup.Text>
                        </InputGroup>
                    </Form.Group>
                </Form>
                <div className="fs-4">Files</div>
                <hr />
                <div className='navbar-nav-scroll' style={{ maxHeight: '70vh', overflowY: 'auto' }}>
                    {filteredFiles.length && filteredFiles.map((file, index) => (
                        <ListGroup.Item key={index} action onClick={() => setSelectedFile(file)}>
                            <div className='d-flex justify-content-between'>
                                <div className='d-flex'>
                                    <span className='me-2'>{handleIcon(file.type)}</span>
                                    <span>{file.name}</span>
                                    <span className='ms-1 text-muted'>({file.type})</span>
                                </div>
                                <div>
                                    <Badge bg="secondary">{handleDatetime(file.timestamp)}</Badge>
                                    <span className='ms-2' onClick={(e) => { e.stopPropagation(); handleDelete(file); }}>
                                        <icons.BsTrash />
                                    </span>
                                </div>
                            </div>
                        </ListGroup.Item>
                    ))}
                </div>
            </ListGroup>
        </>
    );
}
