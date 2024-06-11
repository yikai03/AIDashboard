import React, {useState} from 'react'

const Table = ({tables}) => {
    const [allchecked, setAllChecked] = React.useState([]);

    function handleChange(e) {
       if (e.target.checked) {
          setAllChecked([...allchecked, e.target.value]);
       } else {
          setAllChecked(allchecked.filter((item) => item !== e.target.value));
       }

       console.log(allchecked);
    }

    function handleCheckAll() {
       setAllChecked(tables.map((table) => table.Table));
    }

return (
    <div>
        {tables.map((table, index) => (
            <div key={index} className='grid grid-cols-1 border border-black bg-white rounded mt-3'>
                <div className='border border-green-500 flex flex-row justify-between'>
                    <div>{table.Table}</div>
                    <input
                        value={table.ToTrain}
                        type="checkbox"
                        onChange={handleChange}
                        onClick={table.ToTrain === "Yes" ? () => table.ToTrain = "No" : () => table.ToTrain = "Yes"}
                        checked={table.ToTrain === "Yes"}
                    />
                </div>
            </div>
        ))}
    </div>
);
}

export default Table