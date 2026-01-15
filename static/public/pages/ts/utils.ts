export const getCookie = (name: string): string | undefined => {
  const nameEQ = name + "=";
  // Split the document.cookie string into an array of individual cookies
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    // Trim leading whitespace
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    // If the cookie string starts with the name we're looking for, return its value
    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return undefined; // Return undefined if the cookie is not found
};