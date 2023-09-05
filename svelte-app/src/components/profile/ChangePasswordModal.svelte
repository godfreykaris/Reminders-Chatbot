<script>
    import { push } from "svelte-spa-router";
    import { createEventDispatcher } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';

      let email = '';
      let phone_number = '';
      let oldPassword = '';
      let newPassword = '';
      let confirmNewPassword = '';

      let is_loading = false;
  
      let error_message = ''; // Initialize response message variable
      let success_message = ''; // Initialize response message variable
    
  const dispatch = createEventDispatcher();

  function closeModal() {
    dispatch('closeModal');
  }


    async function changePassword() {

        if (confirmNewPassword !== newPassword) {
            alert('Passwords do not match. Please make sure both passwords match.');
            return;
        }

        if (oldPassword === newPassword) {
            alert('old password is the same as new password');
            return;
        }

        if (!validate_email(email)) {
            alert('Invalid email format. Please enter a valid email address.');
            return;
        }

        if (!validate_phone(phone_number)) {
            alert('Invalid phone number. Please enter a valid phone number.');
            return;
        }

        is_loading = true;

        const formData = {
          phone_number,
          email,
          oldPassword,
          newPassword,
        }
        
        let csrf = document.getElementsByName("csrf-token")[0].content;
        
        const response = await fetch('/api/change_password', {
          method: 'POST',
          credentials: "same-origin",
          headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf,
          },
          body: JSON.stringify(formData),
        });        

        const data = await response.json();

        if (response.ok) 
        {
            // Registration successful
            console.log('Password changed successfully');
            success_message = data.message; // Set the message from the response
            //message = data.message; // Set the error message from the response  
            is_loading = false;
        } 
        else 
        {
            // change failed, handle errors
            error_message = data.message; // Set the error message from the response
            console.error('Password Change failed:');
            is_loading = false;
        } 
        
        closeModal();
  
    }

        function validate_email(email){
            const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return email_regex.test(email);
        }

        function validate_phone(phone){
            const phone_regex = /[0-9]/;
            return phone_regex.test(phone);
        }
    </script>
    
    
    <div class="modal-overlay">
      <div class="modal">
        <!-- Display the message if it's not empty -->
      {#if error_message}
        <p class="error-message">{error_message}</p>
      {:else}
        <p class="success-message">{success_message}</p>
      {/if}
    
        <h1>Change Password</h1>
        
        <form on:submit|preventDefault={changePassword}>
           
            <label for="email">Email</label>
            <input type="email" id="email" bind:value={email} required/>
            
            <label for="phone">Phone</label>
            <input type="phone" id="phone" bind:value={phone_number} required/>
            
            <label for="oldPassword">Old Password</label>
            <input type="password" id="oldPassword" bind:value={oldPassword} required/>
            
            <label for="newPassword">New Password</label>
            <input type="password" id="newPassword" bind:value={newPassword} required/>

            <label for="confirmNewPassword">Confirm New Password</label>
            <input type="password" id="confirmNewPassword" bind:value={confirmNewPassword} required/>
            
            <br>
            {#if is_loading}
              <div class="center-container">
                <Circle2 />
              </div>
            {/if}

            <button type="submit">Change Password</button> 
            <button on:click={closeModal}>Cancel</button>
            <hr/>
          

      </form>
      </div>
    </div>
    
    <style>
      .center-container {
        display: flex;
        flex-direction: column; /* Center vertically */
        justify-content: center; /* Center vertically */
        align-items: center; /* Center horizontally */
      }
    
      input{
        border: solid black 2px;
      }
    
      h1 {
      color: #ff3e00;
      text-transform: uppercase;
      font-size: 2em;
      font-weight: 100;
    }
  
   

    /* Styles for the modal dialog */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000; /* Ensure it's on top of everything */
  }

  .modal {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
  }
      
    </style>
    
    