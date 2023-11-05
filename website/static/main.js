/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/js/main.js":
/*!************************!*\
  !*** ./src/js/main.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _theme__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./theme */ \"./src/js/theme.js\");\n/* harmony import */ var _theme__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_theme__WEBPACK_IMPORTED_MODULE_0__);\n\r\n\n\n//# sourceURL=webpack://frontend/./src/js/main.js?");

/***/ }),

/***/ "./src/js/theme.js":
/*!*************************!*\
  !*** ./src/js/theme.js ***!
  \*************************/
/***/ (() => {

eval("(() => {\r\n    'use strict'\r\n\r\n    const storedTheme = localStorage.getItem('theme')\r\n\r\n    const getPreferredTheme = () => {\r\n        if (storedTheme) {\r\n            return storedTheme\r\n        }\r\n\r\n        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'\r\n    }\r\n\r\n    const setTheme = function (theme) {\r\n        if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {\r\n            document.documentElement.setAttribute('data-bs-theme', 'dark')\r\n        } else {\r\n            document.documentElement.setAttribute('data-bs-theme', theme)\r\n        }\r\n    }\r\n\r\n    setTheme(getPreferredTheme())\r\n\r\n    const showActiveTheme = (theme, focus = false) => {\r\n        const themeSwitcher = document.querySelector('#bd-theme')\r\n\r\n        if (!themeSwitcher) {\r\n            return\r\n        }\r\n\r\n        const themeSwitcherText = document.querySelector('#bd-theme-text')\r\n        const activeThemeIcon = document.querySelector('.theme-icon-active use')\r\n        const btnToActive = document.querySelector(`[data-bs-theme-value=\"${theme}\"]`)\r\n        const svgOfActiveBtn = btnToActive.querySelector('svg use').getAttribute('href')\r\n\r\n        document.querySelectorAll('[data-bs-theme-value]').forEach(element => {\r\n            element.classList.remove('active')\r\n            element.setAttribute('aria-pressed', 'false')\r\n        })\r\n\r\n        btnToActive.classList.add('active')\r\n        btnToActive.setAttribute('aria-pressed', 'true')\r\n        activeThemeIcon.setAttribute('href', svgOfActiveBtn)\r\n        const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`\r\n        themeSwitcher.setAttribute('aria-label', themeSwitcherLabel)\r\n\r\n        if (focus) {\r\n            themeSwitcher.focus()\r\n        }\r\n    }\r\n\r\n    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {\r\n        if (storedTheme !== 'light' || storedTheme !== 'dark') {\r\n            setTheme(getPreferredTheme())\r\n        }\r\n    })\r\n\r\n    window.addEventListener('DOMContentLoaded', () => {\r\n        showActiveTheme(getPreferredTheme())\r\n\r\n        document.querySelectorAll('[data-bs-theme-value]')\r\n            .forEach(toggle => {\r\n                toggle.addEventListener('click', () => {\r\n                    const theme = toggle.getAttribute('data-bs-theme-value')\r\n                    localStorage.setItem('theme', theme)\r\n                    setTheme(theme)\r\n                    showActiveTheme(theme, true)\r\n                })\r\n            })\r\n    })\r\n})()\r\n\n\n//# sourceURL=webpack://frontend/./src/js/theme.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./src/js/main.js");
/******/ 	
/******/ })()
;