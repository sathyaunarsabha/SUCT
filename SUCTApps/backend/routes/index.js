import express from 'express';
import donationRoutes from '../modules/donationmanager/index.js';
import attendanceRoutes from '../modules/attendancetracker/index.js';
import schedulerRoutes from '../modules/zoomscheduler/index.js';

const router = express.Router();
router.use('/donation', donationRoutes);
router.use('/attendance', attendanceRoutes);
router.use('/zoomschedule', schedulerRoutes);
export default router;