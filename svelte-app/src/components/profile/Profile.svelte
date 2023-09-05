<!-- Profile.svelte -->
<script>
    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
    import { push } from 'svelte-spa-router';

    import EditUserModal from './EditUserModal.svelte';
    import ChangePasswordModal from './ChangePasswordModal.svelte';

    let isEditUserModalOpen = false;
    let isChangePasswordModalOpen = false;

    let is_change_password_modal_open = false;
      
    let isLoading = false;
  
    let user = {
      name: '', // Initialize with empty values or defaults
      email: '',
      phone: '',
    };
  
    let error_message = '';
    let success_message = '';

    function open_change_password_modal(){
      is_change_password_modal_open = true;
    }


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
  
      if (response.status === 200) {
        let data = await response.json();
        user = data.user_info;
        isLoading = false;
      }
      else if (response.status === 401) 
      {
        // Redirect to the login page when Unauthorized (401) status is received
        push('/login'); // Replace '/login' with your actual login page URL

      }
      else 
      {
        error_message = "An error occurred trying to fetch your data.";
        success_message = '';
        isLoading = false;
        location.reload();
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
  <ChangePasswordModal  on:closeModal={() => {isChangePasswordModalOpen = false;}} />
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
  <button on:click={openEditUserModal}>Edit User</button>
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

/* Add your custom styles here for the Profile tab */
</style>
  