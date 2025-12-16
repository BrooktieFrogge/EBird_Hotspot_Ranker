import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import HomeScreen from '../views/HomeScreen.vue';
const HotspotSearch = () => import('../views/HotspotSearch.vue');
const HotspotDetail = () => import('../views/HotspotDetail.vue');
const PrintableReport = () => import('../views/PrintableReport.vue');

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'HomeScreen',
    component: HomeScreen,
  },
  {
    path: '/hotspot-search',
    name: 'HotspotSearch',
    component: HotspotSearch,
  },
  {
    path: '/hotspot/:id',
    name: 'HotspotDetail',
    component: HotspotDetail,
  },
  {
    path: '/hotspot/:id/print',
    name: 'PrintableReport',
    component: PrintableReport,
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/',
  }
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;