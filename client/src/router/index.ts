import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
const HotspotSearch = () => import('../views/HotspotSearch.vue');
const HotspotDetail = () => import('../views/HotspotDetail.vue');

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'HotspotSearch',
    component: HotspotSearch,
  },
  {
    path: '/hotspot/:id',
    name: 'HotspotDetail',
    component: HotspotDetail,
  },
  // fallback route
  {
    path: '/:catchAll(.*)',
    redirect: '/',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;