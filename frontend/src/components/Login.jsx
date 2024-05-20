import React, { useState } from 'react';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

const Modal = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate();

    const handleLogin = async () => {
        // Define the API endpoint
        const url = "http://127.0.0.1:8000/login";  // Adjust the URL based on your setup, if needed

        // Make the POST request
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });
            const data = await response.json();

            // Check response status and handle accordingly
            if (data.status === 'success') {
                toast.success("Login successful");  // Show a success message
                console.log(data['UniqueUserID']);
                closeModal();  // Close the modal on successful login
                return navigate('/dataintegration')
                
            } else {
                toast.error("Login failed");
                // Optionally handle login failure (e.g., show an error message)
            }
        } catch (error) {
            console.error("There was an error!", error);
        }
    };


    const [showModal, setShowModal] = useState(false);

    const openModal = () => {
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
    };

    return (
        <div className='flex justify-center items-center h-screen'>
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={openModal}>
                Login
            </button>
        {showModal && (
            <div className="fixed z-10 inset-0 overflow-y-auto">
            <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div className="fixed inset-0 transition-opacity" aria-hidden="true">
                <div className="absolute inset-0 bg-gray-500 opacity-75" onClick={closeModal}></div>
                </div>
                <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" role="dialog" aria-modal="true" aria-labelledby="modal-headline">
                <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <div className="sm:flex sm:items-start">
                    <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 sm:mx-0 sm:h-10 sm:w-10">
                        {/* Icon */}
                    </div>
                    <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                        <h3 className="text-lg leading-6 font-medium text-gray-900" id="modal-headline">
                        Login
                        </h3>
                        <div className="mt-2">
                        <form>
                            <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                            Username:
                            </label>
                            <input type="text" id="username" name="username" className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" value={username} onChange={(e) =>{setUsername(e.target.value)}} />
                            <label htmlFor="password" className="block mt-2 text-sm font-medium text-gray-700">
                            Password:
                            </label>
                            <input type="password" id="password" name="password" className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" value={password} onChange={(e) =>{setPassword(e.target.value)}} />
                        </form>
                        </div>
                    </div>
                    </div>
                </div>
                <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                    <button type="button" onClick={handleLogin} className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm">
                    Login
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
  );
};

export default Modal;