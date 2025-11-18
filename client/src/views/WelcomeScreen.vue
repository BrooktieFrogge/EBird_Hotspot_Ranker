<template>
  <div id="welcome-screen">

    <!-- Settings -->
    <div id="settings-button" class="text-right">
      <button class="settings-btn" @click="toggleSettingsPopup">
        <span><BIconGear /></span>
      </button>
      <div v-if="showSettingsPopup" class="settings-popup">
        <label class="switch">
          <input type="checkbox" :checked="isDarkMode" @change="toggleTheme">
          <span class="slider round"></span>
        </label>
        <span>{{ isDarkMode ? 'Dark Mode' : 'Light Mode' }}</span>
      </div>
    </div>

    <!-- Meeting Browser and Snip Search buttons -->
    <div id="choosing" class="text-center">
      <button class="button" @click="navigateToBrowseMeetings">
        <span><BIconCameraVideoFill class="mr-2" /></span>
        <span>Browse Meetings</span>
      </button>
      <button class="button" @click=" navigateToSnipSearch">
        <span><BIconChatLeftTextFill class="mr-2" /></span>
        <span>Search for Snips</span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { BIconCameraVideoFill, BIconChatLeftTextFill, BIconGear } from 'bootstrap-icons-vue';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'WelcomeScreen',

  components: {
    BIconCameraVideoFill,
    BIconChatLeftTextFill,
    BIconGear
  }

});
</script>

<style scoped>
#welcome-screen {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: url("../../public/welcome_screen_bg.png") no-repeat center center fixed;
  background-size: 100% 100%;
  background-position: top;
}

.row {
  height: 100vh;
}

#settings-button {
  position: absolute;
  top: 20px;
  right: 20px;
}

.settings-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
}

.settings-popup {
  position: absolute;
  top: 40px;
  right: 0;
  background: #333;
  color: white;
  border-radius: 10px;
  padding: 10px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 34px;
  height: 20px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(14px);
}

.slider.round {
  border-radius: 34px;
}

#choosing {
  margin-top: 320px;
}

.button {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 25px;
  height: 40px;
  width: 200px;
  font-size: large;
  font-weight: 250;
  border-radius: 10px;
  border-color: #71e7ff;
  color: #71e7ff;
  background-color: #2061F800;
}

.button .mr-2 {
  margin-right: 15px;
}

.light-mode #welcome-screen {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: url("../../public/welcome_screen_bg_light.png") no-repeat center center fixed;
  background-size: 100% 100%;
}

/* Light mode styles =============================================================================== */
.light-mode .settings-btn {
  color: black;
}

.light-mode .button {
  background-color: #2061F8;
  color: white;
  border-color: #2061F800;
}

.light-mode .settings-popup {
  background: #fff;
  color: #000;
}
</style>
