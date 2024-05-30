import React from 'react'

const SelectDatasetToTrain = () => {
    const [showSelectTrainDataset, setShowSelectTrainDataset] = useState(true)

    const openSelectTrainDataset = () => {
        setShowSelectTrainDataset(true)
    }

    const closeSelectTrainDataset = () => {
        setShowSelectTrainDataset(false)
    }
    
  return (
    <div>SelectDatasetToTrain</div>
  )
}

export default SelectDatasetToTrain