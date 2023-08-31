<script>
  import Router from 'svelte-spa-router';

  import Landing from './components/Landing.svelte';
  import Login from './components/Login.svelte'
  import Register from './components/Register.svelte';
  import Dashboard from './components/Dashboard.svelte';

  import AddGoal from './components/AddGoal.svelte';
  import EditGoal from './components/EditGoal.svelte';
  import DeleteGoal from './components/DeleteGoal.svelte';

  import EditUser from './components/EditUser.svelte';
  import DeleteUser from './components/DeleteUser.svelte';
  import Notfound from  './components/Notfound.svelte';

  import ViewGoals from './components/ViewGoals.svelte';
  import ViewReport from './components/ViewReport.svelte';

  const routes = {
    
    '/': Landing,

    '/login': Login,

    '/register': Register,
    '/edituser': EditUser,
    '/deleteuser': DeleteUser,

    '/dashboard': Dashboard,

    '/addgoal' : AddGoal,
    '/editgoal' : EditGoal,
    '/deletegoal' : DeleteGoal,

    '/viewgoals' : ViewGoals,
    '/viewreport' : ViewReport,

    '*' : Notfound,
}
  
</script>

<Router {routes}/>
