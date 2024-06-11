import React, {useState} from 'react'
import { LuSettings2 } from "react-icons/lu";
import Table from './Table'
import { FaSearch } from "react-icons/fa";


const SelectDatasetToTrain = ({className}) => {
    const [showSelectTrainDataset, setShowSelectTrainDataset] = useState(false)
    const [trainDataset, setTrainDataset] = useState([])

    function handleChange(e) {
       if (e.target.checked) {
          setTrainDataset(trainDataset.map((table) => table.Table === e.target.value ? {...table, ToTrain: "Yes"} : table));
       } else {
          setTrainDataset(trainDataset.map((table) => table.Table === e.target.value ? {...table, ToTrain: "No"} : table));
       }

       console.log(trainDataset);
    }

    const selectTrainDataset = async () => {
      const url = "http://localhost:8000/ai-train"
      const response = await fetch(url)
      const data = await response.json()
      console.log(data)
      setTrainDataset(data)
    }

    const closeModal = () => {
      setShowSelectTrainDataset(false)
    }

    const openModal = () => {
      setShowSelectTrainDataset(true)
    }

    const handleSubmit = () => {
      console.log(trainDataset)
      TrainAI()
      closeModal()
    }

    const TrainAI = async () => {
      const url = "http://localhost:8000/ai-train"
      console.log("This is how the stringify trainDataset looks like :", JSON.stringify(trainDataset))
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(trainDataset)
      })


      const data = await response.json()
      console.log(data.status)

    }

    
    
  return (
    <div>
      <button className='cursor-pointer ml-5' onClick={() => {setShowSelectTrainDataset(!showSelectTrainDataset); 
      selectTrainDataset()
      }}>
        <LuSettings2 className={className}/>
      </button>

      {showSelectTrainDataset && (
        <div className='fixed z-10 inset-0 overflow-auto'>
          <div className='flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center bg-white'>
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
              <div className="absolute inset-0 bg-gray-500 opacity-75" onClick={() => setShowSelectTrainDataset(!showSelectTrainDataset)}></div>
            </div>
            

          </div>
        </div>
      )}

      {showSelectTrainDataset && (
            <div className="fixed z-10 inset-0 overflow-y-auto">
            <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div className="fixed inset-0 transition-opacity" aria-hidden="true">
                <div className="absolute inset-0 bg-gray-500 opacity-75" onClick={closeModal}></div>
                </div>
                <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" role="dialog" aria-modal="true" aria-labelledby="modal-headline">
                <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <div className="sm:flex sm:items-start flex justify-center items-center">
                      <div className="mt-3 flex flex-col justify-center items-center">
                        <div className="mx-auto flex items-center justify-center rounded-full bg-blue-100 sm:mx-0 sm:h-10 sm:w-10">
                            <FaSearch />
                        </div>
                          <h3 className="text-lg leading-6 font-medium text-gray-900" id="modal-headline">
                          Select Dataset to Train
                          </h3>
                          <div className="mt-2 w-full">
                          {trainDataset.map((table, index) => (
                              <div key={index} className='grid grid-cols-1 border border-black bg-white rounded mt-3'>
                                  <div className='border border-green-500 flex flex-row justify-between'>
                                      <div>{table.Table}</div>
                                      <input
                                          value={table.ToTrain}
                                          onChange={handleChange}
                                          type="checkbox"
                                          onClick={table.ToTrain === "Yes" ? () => table.ToTrain = "No" : () => table.ToTrain = "Yes"}
                                          checked={table.ToTrain === "Yes"}
                                      />
                                  </div>
                              </div>
                          ))}
                          </div>
                      </div>
                    </div>
                </div>
                <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                    <button type="button" onClick={handleSubmit} className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm">
                    Select
                    </button>
                    <button type="button" onClick={closeModal} className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 sm:mt-0 sm:w-auto sm:text-sm">
                    Cancel
                    </button>
                </div>
                </div>
            </div>
            </div>
        )}  
    </div>
  )
}

export default SelectDatasetToTrain