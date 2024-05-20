import React from 'react'
import {RocketOutlined} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'


const Logo = () => {
  const navigate = useNavigate();
  return (
    <div className='flex items-center justify-center p-2.5 text-white'>
        <div className='w-10 h-10 flex items-center justify-center text-2xl rounded-lg'>
            <RocketOutlined onClick={() =>{navigate('/')}}/>
        </div>
    </div>
  )

}

export default Logo