import React, {useState} from 'react'
import { LuSettings2 } from "react-icons/lu";

const SelectDatasetToTrain = ({className}) => {
    const [showSelectTrainDataset, setShowSelectTrainDataset] = useState(true)

    const openSelectTrainDataset = () => {
        setShowSelectTrainDataset(true)
    }

    const closeSelectTrainDataset = () => {
        setShowSelectTrainDataset(false)
    }
    
  return (
    <div>
      <LuSettings2 className={className}/>
    </div>
  )
}

export default SelectDatasetToTrain