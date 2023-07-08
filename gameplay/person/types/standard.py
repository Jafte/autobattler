

class GameplayPersonTypeStandard:
    health: int = 100
    strength: int = 10
    mobility: int = 1
    charge: int = 100
    humanness: int = 0
    svg: str = '<svg fill="#000000" width="100%" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M418.18,186.42c0-.09.06-.17.05-.26,0-.32-.26-.56-.35-.86a5.09,5.09,0,0,0-.64-1.56,5.18,5.18,0,0,0-.88-.87c-.28-.25-.46-.6-.8-.79-.16-.09-.34-.06-.5-.13s-.24-.22-.39-.27L339,155.63A77.75,77.75,0,0,0,323.51,127a5.36,5.36,0,0,0-1.42-1.62C296.73,97.75,258,98.53,257.72,98.56h-3.25c-.44-.08-39.23-.89-64.6,26.86a5,5,0,0,0-1,1.12,77.89,77.89,0,0,0-15.83,29.09L97.33,181.68c-.16,0-.24.2-.39.27s-.34,0-.5.13c-.34.19-.52.54-.8.79a5.18,5.18,0,0,0-.88.87,5.09,5.09,0,0,0-.64,1.56c-.09.3-.32.54-.35.86,0,.09,0,.17,0,.26s-.08.19-.08.3V302.09a19.37,19.37,0,0,0,19.35,19.35h11.39a24.43,24.43,0,0,0,11.24-46.11L127,270.82l16.62-34a.5.5,0,0,1,0-.12,5.21,5.21,0,0,0,.52-2.22V220l24.68,14.8c.13.08.28,0,.42.12,4.64,25.1,14.29,47.13,25.74,63.33l-20.72,20.67a5.7,5.7,0,0,0-.47.7,6.71,6.71,0,0,0-.48.58c0,.08,0,.17-.07.24a14.21,14.21,0,0,0-.5,2c0,.07,0,.14,0,.21v45a43.6,43.6,0,0,0-27.44,40.42,5.33,5.33,0,0,0,5.33,5.33h74.92a5.33,5.33,0,0,0,5.33-5.33V391.69a27.14,27.14,0,0,0-17.34-25.26V340.8l13.21-13.21a58.88,58.88,0,0,0,27.52,6.47h3.44a58.88,58.88,0,0,0,27.52-6.47l13.21,13.21v25.63a27.14,27.14,0,0,0-17.34,25.26v16.44a5.33,5.33,0,0,0,5.33,5.33h74.93a5.33,5.33,0,0,0,5.33-5.33,43.61,43.61,0,0,0-27.45-40.42v-45c0-.07,0-.14,0-.21a5.38,5.38,0,0,0-.21-1,5.27,5.27,0,0,0-.29-1c0-.07,0-.16-.07-.24a6.57,6.57,0,0,0-.48-.57,5.82,5.82,0,0,0-.47-.71L317,298.25c11.45-16.2,21.1-38.23,25.74-63.33.13-.07.28,0,.41-.12L367.81,220v14.46a5.21,5.21,0,0,0,.52,2.22.5.5,0,0,1,0,.12l16.62,34-8.69,4.51a24.43,24.43,0,0,0,11.24,46.11h11.39a19.37,19.37,0,0,0,19.35-19.35V186.72C418.26,186.61,418.19,186.53,418.18,186.42Zm-163.9-77.2h3.63c.4,0,32.9-.79,55,21.87l-17,60a55.65,55.65,0,0,0-2.11,15.23v41.47a19.09,19.09,0,0,1-19.07,19.07H257.72a5.22,5.22,0,0,0-1.72.35,5.22,5.22,0,0,0-1.72-.35H237.35a19.09,19.09,0,0,1-19.08-19.07V206.37a55.65,55.65,0,0,0-2.11-15.23L199.08,131C219,110.4,247.24,109.2,253.23,109.2,253.77,109.2,254.13,109.22,254.28,109.22ZM133.52,229.12H104.4v-33l29.12,17.47Zm4.72,67.9a13.77,13.77,0,0,1-13.76,13.76H113.09a8.7,8.7,0,0,1-8.69-8.69V277.57h12.49l13.92,7.22A13.75,13.75,0,0,1,138.24,297Zm-21.18-30.11H104.4V239.79h25.92ZM141.6,206h0l-15.22-9.12L111.63,188l58.26-20a172.75,172.75,0,0,0-2.51,53.48Zm41.81,158.5v-33l19.47,10.27v22.71H183.41Zm36.82,27.17v11.1H156.4a33,33,0,0,1,32.51-27.61h14.82A16.52,16.52,0,0,1,220.23,391.69Zm-13-59.65L187,321.35l14.64-14.6c.14.16.27.34.41.5a98.59,98.59,0,0,0,15.53,14.47Zm148.38,70.75H291.77v-11.1a16.52,16.52,0,0,1,16.5-16.51h14.82A33,33,0,0,1,355.61,402.79Zm-46.49-38.27V341.81l19.47-10.27v33H309.12ZM325,321.35,304.77,332l-10.32-10.32A98.63,98.63,0,0,0,310,307.25c.14-.16.27-.34.41-.5ZM302,300.22c-14.25,16.25-27.49,23.18-44.25,23.18h-3.44c-16.76,0-30-6.93-44.24-23.18-24-27.33-42.85-82.48-27.64-139A72.42,72.42,0,0,1,191,141.47l14.92,52.58a44.69,44.69,0,0,1,1.72,12.32v41.47a29.76,29.76,0,0,0,29.74,29.73h16.93a5.21,5.21,0,0,0,1.72-.34,5.21,5.21,0,0,0,1.72.34h16.94a29.76,29.76,0,0,0,29.73-29.73V206.37a44.57,44.57,0,0,1,1.72-12.31L321,141.54a71.05,71.05,0,0,1,8.6,19.67C344.81,217.73,325.94,272.89,302,300.22ZM342.12,168l58.25,20-14.75,8.86L370.41,206h0l-25.77,15.46A172.75,172.75,0,0,0,342.12,168Zm65.48,61.12H378.48V213.6l29.12-17.47Zm0,10.67v27.12H394.94l-13.26-27.12Zm-8.69,71H387.52a13.77,13.77,0,0,1-6.33-26l13.93-7.22H407.6v24.52A8.7,8.7,0,0,1,398.91,310.78Z"/><path d="M231,165.16h46.64a5.33,5.33,0,0,0,0-10.66H231a5.33,5.33,0,0,0,0,10.66Z"/></svg>'