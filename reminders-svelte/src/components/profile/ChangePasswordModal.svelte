<script>
    // @ts-ignore
    import { push } from "svelte-spa-router";
    import { Circle2 } from 'svelte-loading-spinners';
    import { EyeOutline, EyeSlashOutline } from 'flowbite-svelte-icons'
    import { Button, Label, Input } from 'flowbite-svelte';

    let email = '';
    let phone_number = '';
    let oldPassword = '';
    let newPassword = '';
    let confirmNewPassword = '';

    let isLoading = false;
  
    let errorMessage = ''; // Initialize response message variable
    let successMessage = ''; // Initialize response message variable
    
    let showPassword = false;
    let showNewPassword = false;
    let showConfirmNewPassword = false;

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

        isLoading = true;

        const formData = {
          phone_number,
          email,
          oldPassword,
          newPassword,
        }
        
        // @ts-ignore
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
            successMessage = data.message; // Set the message from the response
            //message = data.message; // Set the error message from the response  
            isLoading = false;
        } 
        else 
        {
            // change failed, handle errors
            errorMessage = data.message; // Set the error message from the response
            console.error('Password Change failed:');
            isLoading = false;
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

        function togglePasswordVisibility() {
            showPassword = !showPassword;
        }

        function toggleNewPasswordVisibility() {
            showNewPassword = !showNewPassword;
        }
        function toggleConfirmNewPasswordVisibility() {
            showConfirmNewPassword = !showConfirmNewPassword;
        }
        
    </script>
    
    
    <style>
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
    
    
    <form class="flex flex-col space-y-6" action="#">
      <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Reminders  </h3>
      <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Change Password</h3>
      
    
      <Label class="space-y-2">
        <span>Email</span>
        <Input type="email" name="email" bind:value={email} placeholder="name@company.com" class="border-1 border-black" required />
      </Label>
      <Label class="space-y-2">
        <span>Phone</span>
        <Input type="tel" name="phone" bind:value={phone_number} placeholder="(123) 456-7890" class="border-1 border-black" required />
      </Label>
      <Label class="space-y-2">
          <strong><span>Old Password</span></strong>
          <div class="relative">
              <Input type={showPassword ? 'text' : 'password'} name="password" bind:value={oldPassword} placeholder="•••••" class="border-1 border-black focus:ring-blue-500 focus:border-blue-500" required />            
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <span on:click={togglePasswordVisibility} class="cursor-pointer absolute inset-y-0 right-0 flex items-center px-2">
                  {#if showPassword}
                      <EyeOutline/>
                  {:else}
                      <EyeSlashOutline/>
                  {/if}
              </span>
          </div>
      </Label>

      <Label class="space-y-2">
        <strong><span>New Password</span></strong>
        <div class="relative">
          <Input type={showNewPassword ? 'text' : 'password'} name="password" bind:value={newPassword} placeholder="•••••" class="border-1 border-black focus:ring-blue-500 focus:border-blue-500" required />
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <span on:click={toggleNewPasswordVisibility} class="cursor-pointer absolute inset-y-0 right-0 flex items-center px-2">
              {#if showNewPassword}
                  <EyeOutline/>
              {:else}
                  <EyeSlashOutline/>
              {/if}
          </span>
        </div>
      </Label>

      <Label class="space-y-2">
        <strong><span>Confirm New Password</span></strong>
        <div class="relative">
          <Input type={showConfirmNewPassword ? 'text' : 'password'} name="confirm-password" bind:value={confirmNewPassword} placeholder="•••••" class="border-1 border-black focus:ring-blue-500 focus:border-blue-500" required />
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <span on:click={toggleConfirmNewPasswordVisibility} class="cursor-pointer absolute inset-y-0 right-0 flex items-center px-2">
              {#if showConfirmNewPassword}
                  <EyeOutline/>
              {:else}
                  <EyeSlashOutline/>
              {/if}
          </span>
        </div>
      </Label>
      <!-- Show loading indicator while isLoading is true -->
      {#if isLoading}
        <div class="flex items-center justify-center">
          <Circle2 size="64" />
        </div>
      {/if}
      
      <!-- Display error or success message based on conditions -->
      {#if errorMessage}
        <p class="error-message">{errorMessage}</p>
      {:else if successMessage}
        <p class="success-message">{successMessage}</p>
      {/if}
      <Button on:click={changePassword} class="w-full1">Update Profile</Button>
    </form>