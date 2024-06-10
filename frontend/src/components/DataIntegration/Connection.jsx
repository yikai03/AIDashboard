import React, {useEffect, useState} from 'react'
import {TfiReload} from "react-icons/tfi"
import { MdKeyboardArrowDown, MdKeyboardArrowUp } from "react-icons/md";
import { LuSave } from "react-icons/lu";
import Table from './Table'
import {toast} from 'react-toastify'

const Connection = ({connection, opacity}) => {
    const [IsExpanded, setIsExpanded] = useState(false)
    const [IsReloaded, setIsReloaded] = useState(false)
    const [description, setDescription] = useState(connection.Description)
    const [sampleData, setSampleData] = useState([])

    const toggleExpand = () => {
        setIsExpanded(!IsExpanded)
        console.log("clicked")
        {IsExpanded ? console.log("expanded") : console.log("not expanded")}
    }

    useEffect(() => {
        toggleReload(connection.ConnectionID)
    }, [])

    const toggleReload = async(ConnectionID) => {
        // const url = `http://localhost:8000/sql-query-top?ID=${ConnectionID}`
        const url = "http://localhost:8000/sql-query-top"
        console.log(ConnectionID)
        // const info = {ID: ConnectionID}
        try{
            const response = await fetch(url,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ID: ConnectionID})
            })
            if (!response.ok) {
                throw new Error('Network response was not ok');
              }
            
            const data = await response.json()
            console.log(data)
            setSampleData(data)
            setIsReloaded(!IsReloaded)
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    const toggleSave = async(ConnectionID) => {
        const url = "http://localhost:8000/add-description"
        try{
            const response = await fetch(url,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ID: ConnectionID, Description: description})
                }
            )
            const data = await response.json()
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            if(data.status == "success"){
                toast.success("Description saved successfully")       
                console.log("Description saved successfully")         
            }
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }

        console.log("saved")
    }

    //Await for desription (Done)

    //Await for passing SQL to get sample data (Done)

    //Await for connection status (Require to understand why need this)

    //Await for statistical analysis (if needed)

    //Await for manual select columns (if needed)

    return (
        <div className={opacity}>
            <div className=' drop-shadow-xl overflow-hidden bg-white border-x-[0.5px] border-gray-400 rounded mt-1 mb-2 transition hover:-translate-y-1 ease-in-out duration-300'>

                <div className='flex justify-between'>        
                    <div className='text-2xl ml-1 font-bold w-32'>{connection.Table}</div>
                    {/* <div className='text-2xl font-bold w-24'>{connection.ConnectionStatus}</div> */}

                    {/* <TfiReload className='text-2xl cursor-pointer self-center' onClick={() => toggleReload(connection.ConnectionID)}/> */}

                    {IsExpanded ? <MdKeyboardArrowUp className="text-2xl self-center cursor-pointer" onClick={toggleExpand} /> : <MdKeyboardArrowDown className="text-2xl self-center cursor-pointer" onClick={toggleExpand} />}
                </div>


                <div className={`overflow-hidden transition-all ease-in-out duration-[500ms] ${IsExpanded ? " max-h-[500px] opacity-100" : "max-h-0 opacity-0"}`}>
                    <div className='p-2'>
                        <label htmlFor="description" className='overflow-hidden mr-2 text-1xl font-bold'>Description:</label>
                        <input className='border border-black rounded w-96 ' id="description" name="description" value={description} onChange={(e) => setDescription(e.target.value)}></input>
                        <LuSave className='cursor-pointer inline ml-2 text-2xl' onClick={() =>toggleSave(connection.ConnectionID)}/>
                        <Table sampleData={sampleData}/>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Connection