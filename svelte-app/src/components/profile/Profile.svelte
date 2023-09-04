<!-- Profile.svelte -->
<script>
    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
    import { push } from 'svelte-spa-router';

    import EditUserModal from './EditUserModal.svelte'; // Adjust the path to your component
    import ChangePassword from './ChangePassword.svelte';

    let isEditUserModalOpen = false;

    let is_change_password_modal_open = false;

    function open_change_password_modal(){
      is_change_password_modal_open = true;
    }

    function close_change_password_modal(){
      is_change_password_modal_open = false;
    }
  
      
    let isLoading = false;
  
    let user = {
      name: '', // Initialize with empty values or defaults
      email: '',
      phone: '',
    };
  
    let error_message = '';
    let success_message = '';

    function openEditUserModal() {
      isEditUserModalOpen = true;
    }
  
    async function fetchUser() {
      isLoading = true;
      // Fetch the current user's data
      const response = await fetch(`/api/user_data`, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
          'Accept': 'application/json',
          'X-CSRFToken': document.getElementsByName("csrf-token")[0].content,
        },
      });
  
      if (response.ok) {
        const user_data = await response.json();
        user = user_data['user_info'];
        isLoading = false;
      } else {
        error_message = "An error occurred fetching user";
        success_message = '';
        isLoading = false;
      }
    }
  
    async function logout() {
      isLoading = true;
      await fetch('/api/logout', {
        method: 'GET',
        credentials: 'same-origin',
      })
        .then(response => response.json())
        .then(data => {
          if (data.logout) {
            push('/login'); // Redirect to the login page on successful logout
          } else {
            console.log('Logout failed');
          }
        })
        .catch(error => {
          console.error('Error:', error);
        })
        .finally(() => {
          isLoading = false;
        });
    }
  
    onMount(() => {
      fetchUser(); // Fetch user data when the component is mounted
    });
  </script>
  
<!-- Edit User Modal -->
{#if isEditUserModalOpen}
  <EditUserModal editedUser={user} on:closeModal={() => {isEditUserModalOpen = false; fetchUser()}} />
{/if}

<!--Change password modal-->
{#if is_change_password_modal_open}  
    <div class="modal">
      <div class="modal-content">
        <button on:click={close_change_password_modal}>&times;</button>
        <ChangePassword/>
      </div>
    </div>
{/if}


<main class="center-container">

{#if error_message != ''}
  <p class="error-message">{error_message}</p>
{:else if success_message != ''}
  <p class="success-message">{success_message}</p>
{/if}

{#if isLoading}
  <div class="center-container">
    <Circle2 size="64" />
  </div>
{:else}
  <p><strong>Name:</strong> {user.name}</p>
  <p><strong>Email:</strong> {user.email}</p>
  <p><strong>Phone:</strong> {user.phone}</p>

  <hr />

  <button on:click={open_change_password_modal}>Change Password</button>
  <button on:click={openEditUserModal}>Edit Profile</button>
  <button on:click={logout}>Logout</button>
{/if}



</main>

<style>
main {
  text-align: center;
  padding: 1em;
  max-width: 240px;
  margin: 0 auto;
}

.center-container {
        display: flex;
        flex-direction: column; /* Center vertically */
        justify-content: center; /* Center vertically */
        align-items: center; /* Center horizontally */
    }

    .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
    z-index: 1;
    overflow: auto;
  }

  /* Modal content styles */
  .modal-content {
    position: relative;
    margin: 15% auto; /* Center the modal vertically */
    width: 60%;
    max-width: 400px; /* Limit the modal width */
    background-color: #fcfafd;
    padding: 20px;
    box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.2); /* Box shadow for a subtle elevation effect */
    border-radius: 8px;
  }

  /* Close button styles */
  .modal-content button {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: transparent;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }

/* Add your custom styles here for the Profile tab */
</style>
  