<script>
    import { Circle2 } from 'svelte-loading-spinners';
    import { createEventDispatcher } from 'svelte';


    let email = '';
    let phone_number = '';
    let is_loading = false;

    const dispatch = createEventDispatcher();

  function closeModal() {
    dispatch('closeModal');
  }

    async function resetPassword() {
        if (!validate_email(email)) {
            alert('Invalid email format. Please enter a valid email address.');
            return;
        }

        if (!validate_phone(phone_number)) {
            alert('Invalid phone number. Please enter a valid phone number.');
            return;
        }        

        is_loading = true;

        let csrf = document.getElementsByName("csrf-token")[0].content;

        const response = await fetch('/api/reset_password', {
            method: "POST",
            credentials: "same-origin",
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf,
            },
            body: JSON.stringify({ email, phone_number }),
        });

        is_loading = false;

        const data = response.json()

        if (response.ok) {
            alert('A new password has been sent to your email, check your inbox');
        } else {
            alert('Password reset failed, please try again later', data.message);
        }


        closeModal();
    }

    function validate_email(email) {
        const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return email_regex.test(email);
    }

    function validate_phone(phone) {
        const phone_regex = /[0-9]/;
        return phone_regex.test(phone);
    }
</script>

<div class="modal-overlay">
    <div class="modal">
    <h1>Reset Password</h1>
    <form on:submit={resetPassword}>
        <label for="email">Email:</label>
        <input type="email" id="email" bind:value={email} required />
      
        <label for="phone">Phone Number:</label>
        <input type="tel" id="phone" maxlength="13" bind:value={phone_number} required />
      
        {#if is_loading}
            <div class="center-container">
              <Circle2 />
            </div>
        {/if}

        <br/>

        <button type="submit" disabled={is_loading}>Reset Password</button>
        <button on:click={closeModal}>Cancel</button>
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

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 2em;
		font-weight: 100;
	}

	
</style>
