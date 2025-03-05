/* eslint-disable no-unused-vars */
// src/tauri-dialog-shim.js
export async function confirm(message) {
  return window.confirm(message);
}

export async function message(messageText) {
  return window.alert(messageText);
}