import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import SideBarMenu from './components/SideBar/SideBarMenu.jsx'
import { BrowserRouter } from 'react-router-dom'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <SideBarMenu />
    </BrowserRouter>
  </React.StrictMode>,
)
