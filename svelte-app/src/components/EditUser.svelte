<script>
    let user = {};

    let user_id = 6;

    let selected_user = null;

    let error_message = '';
    let success_message = '';

    async function fetchUser(user_id) {
        const response = await fetch(`http://localhost:5000/get_user/${user_id}`);
        
        if (user.hasOwnProperty('message') && user.message === 'User not found' || user.message === 'Failed to fecth user') {
        // Handle the case where the user is not found
            error_message = "User not found";
            success_message = '';
            user = {};            
        } else {
        // Handle the case where the user is found
            user = await response.json()
        }
    }

    async function select_user(user){
        selected_user = user;
    }

    async function EditUser() {
        const response = await fetch('http://localhost:5000/edit_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }, 
            body: JSON.stringify(selected_user)
        });

        if(!response.ok){
            error_message = "Error editing user";
            success_message = '';
        }else{
            error_message = "";
            success_message = 'User edited successfully';
        }

        // const data = await response.json();
        // console.log(data.message);
    }

    //email and phone validation
    function validate_email(email){
        const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return email_regex.test(email);
    }

    function validate_phone(phone){
        const phone_regex = /[0-9]/;
        return phone_regex.test(phone);
    }

</script>

<main>
    <h1>Edit User</h1>
    <button on:click= {() => fetchUser(user_id)}>Fetch User</button>
    
    {#if error_message != ''}
        <p class="error-message">{error_message}</p>
    {:else if success_message != ''}
        <p class="success-message">{success_message}</p>
    {/if}

    {#if Object.keys(user).length > 0}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <p class="user-list user-item" on:click={() => select_user(user)}>
            {user.email} 
        </p>
    {:else}
        <p>No User found</p>
    {/if}

    {#if selected_user !== null}
    <form on:submit|preventDefault={EditUser}> 
        <h1>Edit User</h1>
        <hr/>
        <label>
            <label>
                Name: <input type="text" bind:value={selected_user.name} required />
            </label>

            Email: <input type="text" bind:value={selected_user.email} required />
            {#if selected_user.email && !validate_email(selected_user.email)}
                <p class="error-message">Invalid email</p>
            {/if}
        </label>
        <label>
            Phone: <input bind:value={selected_user.phone_number} maxlength="13" required />
            {#if selected_user.phone_number && !validate_phone(selected_user.phone_number)}
                <p class="error-message">Invalid phone number</p>
            {/if}
        </label>
        
        <button type="submit">Update User</button>
    </form>
    {/if}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

    .user-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }

     .user-item {
        background-color: #f4f4f4;
        border: 1px solid #ddd;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
        transition: background-color 0.3s ease-in-out;
    }

    .user-item:focus,
    .user-item:hover {
        background-color: #e0e0e0;
        outline: none;
    } 

    .error-message {
        color: red;
        font-size: 14px;
        margin-top: 4px;
    }

    .success-message {
        color: green;
        font-size: 14px;
        margin-top: 4px;
    }
</style>