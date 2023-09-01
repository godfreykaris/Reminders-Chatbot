<script>
    import {push} from 'svelte-spa-router';

    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';

    let isLoading = false;

    let user_data = null;
    let user = {
        name: '', // Initialize with empty values or defaults
        email: '',
        phone: '',
    };

    let error_message = '';
    let success_message = '';


    let headers = new Headers();

    headers.append('Accept', 'application/json');
    let csrf = document.getElementsByName("csrf-token")[0].content;
    headers.append("X-CSRFToken", csrf);

    const myInit = {
      method: "GET",
      credentials: "same-origin",
      headers: headers,
    };

    async function fetchUser() {
         isLoading = true;
         // Get the current user
         const response = await fetch(`/api/user_data`, myInit);
 
         if(response.ok){
             user_data = await response.json();
             user = user_data['user_info'];
             isLoading = false;
         }else{
             error_message = "An error occurred fetching user";
             success_message = '';
             isLoading = false;
         }
    }

    fetchUser();

    async function EditUser() {

        isLoading = true;
        let csrf = document.getElementsByName("csrf-token")[0].content;
        const response = await fetch('/api/edit_user', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf,
            },
            body: JSON.stringify({
              user
            }),  
        });

        if(!response.ok){
            error_message = "Error editing user";
            success_message = '';
            isLoading = false;
        }else{
            error_message = "";
            success_message = 'User edited successfully';
            isLoading = false;
        }

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

<main class="center-container">
    <button on:click={() => push('/dashboard')}>Dashboard</button>
        
    {#if error_message != ''}
        <p class="error-message">{error_message}</p>
    {:else if success_message != ''}
        <p class="success-message">{success_message}</p>
    {/if}

    {#if isLoading}
        <div class="center-container">
            <Circle2 size="64" />
        </div>
    {/if}

    {#if user_data !== null}
    <form on:submit|preventDefault={EditUser}> 
        <h1>Edit User</h1>
        <hr/>
        <label>
            <label>
                Name: <input type="text" bind:value={user['name']} required />
            </label>

            Email: <input type="text" bind:value={user['email']} required />
            {#if user['email'] && !validate_email(user['email'])}
                <p class="error-message">Invalid email</p>
            {/if}
        </label>
        <label>
            Phone: <input bind:value={user['phone']} maxlength="13" required />
            {#if user['phone'] && !validate_phone(user['phone'])}
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

    .center-container {
        display: flex;
        flex-direction: column; /* Center vertically */
        justify-content: center; /* Center vertically */
        align-items: center; /* Center horizontally */
        
      }
    
</style>