import React from 'react'
import { CircleLoader } from 'react-spinners'

const Loader = ({loading}) => {
  return (
    <CircleLoader color='#000000' loading={loading} size={50} />
  )
}

export default Loader