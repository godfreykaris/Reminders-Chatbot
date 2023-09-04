<script>
    import { push } from "svelte-spa-router";
    import { Circle2 } from 'svelte-loading-spinners';

      let email = '';
      let phone_number = '';
      let oldPassword = '';
      let newPassword = '';
      let confirmNewPassword = '';

      let is_loading = false;
  
      let error_message = ''; // Initialize response message variable
      let success_message = ''; // Initialize response message variable
    
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
    
    
    <main>
      <div class="center-container">
        <!-- Display the message if it's not empty -->
      {#if error_message}
        <p class="error-message">{error_message}</p>
      {:else}
        <p class="success-message">{success_message}</p>
      {/if}
    
        <h1>Change Password</h1>
        
        <form>
           
            <label for="email">Email</label>
            <input type="email" id="email" bind:value={email} />
            
            <label for="phone">Phone</label>
            <input type="phone" id="phone" bind:value={phone_number} />
            
            <label for="oldPassword">Old Password</label>
            <input type="password" id="oldPassword" bind:value={oldPassword} />
            
            <label for="newPassword">New Password</label>
            <input type="password" id="newPassword" bind:value={newPassword} />

            <label for="confirmNewPassword">Confirm New Password</label>
            <input type="password" id="confirmNewPassword" bind:value={confirmNewPassword} />
            
            <br>
            {#if is_loading}
              <div class="center-container">
                <Circle2 />
              </div>
            {/if}

            <button on:click={changePassword} disabled={is_loading}>Change Password</button> 
            <hr/>
          
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-missing-attribute -->
        <a on:click={() => push('/login')}>Go back to login</a>
      </form>
      </div>
    </main>
    
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
  
    a{
      cursor: pointer;
    }
      
    </style>
    
    