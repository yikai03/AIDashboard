import React, {useState} from 'react'
import { Menu } from 'antd'
import { useNavigate } from 'react-router-dom';

import {DatabaseOutlined,
    OpenAIOutlined,
    LineChartOutlined,
    InteractionOutlined,
    UserOutlined
} from '@ant-design/icons'


const MenuList = () => {
    const navigate = useNavigate();

  return (
    <Menu theme='dark' mode='inline' className='h-screen mt-8 flex flex-col gap-4 text-base relative'>

        <Menu.Item key="DataIntegration" icon={<DatabaseOutlined />} onClick={() => navigate("DataIntegration")}>
            Data Integration Interface
        </Menu.Item>
        <Menu.Item key="AI" icon={<OpenAIOutlined />} onClick={() => navigate("AI")}>
            AI Query Facilitation Interface
        </Menu.Item>    
        <Menu.Item key="PredictiveAnalysis" icon={<LineChartOutlined />} onClick={() => navigate("PredictiveAnalysis")}>
            Predictive Analytics Visualization Interface
        </Menu.Item>
        <Menu.Item key="UserInteraction" icon={<InteractionOutlined />} onClick={() => navigate("UserInteraction")}>
            Advanced User Interaction Platform
        </Menu.Item>
        <Menu.Item key="UserManagement" icon={<UserOutlined />} onClick={() => navigate("UserManagement")}>
            User Management Interface
        </Menu.Item>

    </Menu>
  )
}

export default MenuList