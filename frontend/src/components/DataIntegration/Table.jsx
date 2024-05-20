import React, {useState} from 'react'

const Table = ({sampleData}) => {
  const [data, setdata] = useState([])

  const getColumnNames = () => {
    if (sampleData.length === 0) return [];
    return Object.keys(((Object.values(sampleData))[0])[0]);
  };

  const getRowData = () => {
    if (sampleData.length === 0) return [];
    return Object.values(((Object.values(sampleData))[0]).map((row) => Object.values(row)).map((row) => row.map((cell) => cell)));
  }

  const getData =() => {
    // console.log(Object.values(Object.values((Object.values(sampleData))[0])[1]))
    console.log(getRowData())
  }
  return (
    <table className="table-fixed w-full border-collapse border border-gray-300 mt-2">
      <thead >
        <tr className="bg-gray-200">
          {getColumnNames().map((columnName, key) => (
            <th key={key} className="px-4 py-2">{columnName}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {getRowData().map((row, key) => (
          <tr key={key} className="{key % 2 === 0 ? 'bg-gray-100' : 'bg-white'} hover:bg-gray-200">
            {row.map((cell, key) => (
              <td key={key} className="px-4 py-2 border border-gray-300">{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>

    // <>
    //   <button onClick={getData}>kkk</button>
    // </>
  )
}

export default Table