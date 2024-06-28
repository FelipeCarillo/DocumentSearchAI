import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import NavBar from './components/NavBar';
import FileManage from './pages/FileManage';
import UploadFileModal from './components/UploadFileModal';

export default function App() {

  const [show, setShow] = useState(false);

  return (
    <div style={{ height: '100vh' }} className='overflow-hidden'>
      <NavBar setShow={setShow} />
      <Router>
        <Routes>
          <Route path="/" element={<FileManage />} />
        </Routes>
      </Router>
      <UploadFileModal show={show} setShow={setShow} />
    </div>
  );
}