import React from 'react'
import {Route, createBrowserRouter, createRoutesFromElements, RouterProvider} from 'react-router-dom'
import SideBarMenu from './components/SideBar/SideBarMenu'
import Hero from './components/Hero'
import HomePage from './pages/HomePage'
import MainLayout from './layout/MainLayout'  
import MenuList from './components/SideBar/MenuList'

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route index element={<HomePage />} />  
      <Route path='/about' element={<div>Aboutaeraraaaaaaaaaaaaaaaaaaaaaaaaaaaa</div>} />
      <Route path='/data-integration' element={<MenuList />} />
      <Route path='/AI' element={<MenuList />} />
      <Route path='/predictive-analysis' element={<MenuList />} />
      <Route path='/user-interaction' element={<MenuList />} />
      <Route path='/user-management' element={<MenuList />} />
    </>
)
)

const App = () => {
  return (
    <RouterProvider router={router}/>
  )
}

export default App