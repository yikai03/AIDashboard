import React, { useState } from 'react'
import {Layout} from 'antd'
import {MenuFoldOutlined, MenuUnfoldOutlined} from '@ant-design/icons'
import Logo from './Logo'
import MenuList from './MenuList'
import { Button, theme} from 'antd'
import App from '../../App'
import {Route, createBrowserRouter, createRoutesFromElements, RouterProvider, Routes} from 'react-router-dom'

import HomePage from '../../pages/HomePage'
import DataIntegration from '../../pages/DataIntegration'
import AI from '../../pages/AI'
import PredictiveAnalysis from '../../pages/PredictiveAnalysis'
import UserInteraction from '../../pages/UserInteraction'
import UserManagement from '../../pages/UserManagement'
// import { Header } from 'antd/es/layout/layout'

const {Header, Sider} = Layout

const SideBarMenu = () => {
  const [collapsed, setCollapsed] = useState(false)
  
  const toggleCollapsed = () => {
    setCollapsed(!collapsed);
  };

  const {
    token:{colorBgContainer},
  } = theme.useToken();

  return (
      <Layout>
          <Sider collapsed={collapsed} collapsible trigger={null} className='text-white text-xl'> 
            <Logo />
            <MenuList />
          </Sider>
          <Layout>
              <Button type='default' className="toggle absolute ml-2 mt-2" onClick={toggleCollapsed} icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} />
                <Routes>
                  <Route index element={<HomePage />} />
                  <Route path='/dataintegration' element={<DataIntegration />} />
                  <Route path='/AI' element={<AI />} />
                  <Route path='/predictiveanalysis' element={<PredictiveAnalysis />} />
                  <Route path='/userinteraction' element={<UserInteraction />} />
                  <Route path='/usermanagement' element={<UserManagement />} />
                </Routes> 
          </Layout>
      </Layout>

  )
}

export default SideBarMenu