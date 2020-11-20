import Vue from "vue";
import Router from "vue-router";
import NavPage from "./views/NavPage.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "navPage",
      component: NavPage
    },{
      path: "/boxes",
      name: "Boxes",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Boxes.vue")
    },
    {
      path: "/bills",
      name: "Bills",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Bills.vue")
    }
  ]
});
