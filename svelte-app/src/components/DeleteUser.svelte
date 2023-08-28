<script>

    let users = [];

    let selected_user = null;

    let error_message = '';
    let success_message = '';

    async function fetchUsers() {
        const response = await fetch('http://localhost:5000/get_users');

        if(response.ok){
            users = await response.json();
            error_message = '';
            success_message = 'Users fetched successfully';

        }else{
            error_message = "An error occurred trying to fetch goals";
            success_message = '';
        }
        
    }

    async function select_user(user){
        selected_user = user;
    }

    async function DeleteUser() {
        if(!selected_user)
            return;

        const confirm_delete = window.confirm("Are you sure you want to delete this user");

        if(!confirm_delete)
            return

        const response = await fetch('http://localhost:5000/delete_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }, 
            body: JSON.stringify({id: selected_user.id})
        });

        if(!response.ok){
            error_message = "Error trying to delete user";
            success_message = '';
        }
        else
        {
            error_message = '';
            success_message = 'User deleted successfully';

        }

        // const data = await response.json();
        // console.log(data.message);

        selected_user = null;
        fetchUsers(); // Refresh the userss list after deletion
    }

</script>

<main>
    <h1>Delete User</h1>

    {#if error_message != ''}
        <p class="error-message">{error_message}</p>
    {:else if success_message != ''}
        <p class="success-message">{success_message}</p>
    {/if}

    <button on:click= {fetchUsers}>Fetch Users</button>

    {#if users.length > 0}
        <ul class="user-list">
            {#each users as user}
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                <li
                    class="user-item"
                    on:click={() => select_user(user)}
                    on:keydown={(event) => {
                        if (event.key === 'Enter' || event.key === 'Space') {
                            select_user(user);
                        }
                    }}
                    tabindex="-1" 
                    > <!--Make the li element focusable-->
                    {user.email}
                </li>
            {/each}
        </ul>
    {:else}
        <p>No users fetched</p>
    {/if}


    {#if selected_user !== null}
        <button on:click={DeleteUser}>Delete User</button>
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

    button{
        background-color: #ff150088;
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