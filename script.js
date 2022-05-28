import VideoFeed from 'video'

// Define a state the get the list of the employee's data
const [employeeList, setEmployeeList] = useState([]);
// Define a state to get the error if there is
const [errorMessage, setErrorMessage] = useState(null);
// Function to send the employee's name (value of an input fiel) and get back his data
const searchForEmployee = () => {
    // Value of the employee's name input
    const name = document.getElementById('searchForEmployee').value.toLowerCase()
    if(name){
        fetch(`http://127.0.0.1:5000/get_employee/${name}`)
        .then(response => response.json())
        .then(response => {
            if(response){
                // Set employeeList state with the response as a json
                setEmployeeList(response)
            } else {
               // Set errorMessage state with the response as a json 
              setErrorMessage(response.Error)
            }
        })
    }
    else{
       setEmployeeList(['No name find...'])
    }
}

// Make the request to the API and get the 5 last entries as a json
const searchForLastEntries = () => {
    fetch('http://127.0.0.1:5000/get_5_last_entries')
    .then(response => response.json())
    .then(response => {
        if(response) {
            // Set the value of the employeeList state with the response
            setEmployeeList(response)
        }
    })
}

// Create a state to check if the user as been added
const [isUserWellAdded, setIsUserWellAdded] = useState(false);
// Create a state to check if the is error while the user's adding
const [errorWhileAddingUser, seterrorWhileAddingUser] = useState(false);
const addEmployeeToDb = e => {
        e.preventDefault()
        // Send it to backend -> add_employee as a POST request
        let name = document.getElementById("nameOfEmployee").value
        let picture = document.getElementById('employeePictureToSend')
        let formData  = new FormData();
        formData.append("nameOfEmployee", name)
        formData.append("image", picture.files[0])
        fetch('http://127.0.0.1:5000/add_employee',{
            method: 'POST',
            body:  formData,
        })
            .then(reposonse => reposonse.json())
            .then(response => {
                console.log(response)
                setIsUserWellAdded(true)
            })
            .catch(error => seterrorWhileAddingUser(true))
    }

    // Get the list of all the employee's in the folder
const getEmployeeList = () => {
    fetch('http://127.0.0.1:5000/get_employee_list')
        .then(response => response.json())
        .then (response => {
            if(!isEmployeeListLoaded){
                setNameList(response)
                setIsEmployeeListLoaded(true)
            }
        })
}
// A Component to have a button that delete the employye:
const EmployeeItem = props => {
    // Function that send the employee's name to delete
    const deleteEmployee = name => {
        fetch(`http://127.0.0.1:5000/delete_employee/${name}`)
            .then(response => response.json())
            .then(() => setIsEmployeeListLoaded(false))
    }
    return(
        <li> { props.name } <ItemButton onClick={ () => deleteEmployee(props.name) }>DELETE</ItemButton></li>
    )
}