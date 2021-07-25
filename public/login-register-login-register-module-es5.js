function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["login-register-login-register-module"], {
  /***/
  "./src/app/login-register/login-register-routing.module.ts":
  /*!*****************************************************************!*\
    !*** ./src/app/login-register/login-register-routing.module.ts ***!
    \*****************************************************************/

  /*! exports provided: LoginRegisterRoutingModule */

  /***/
  function srcAppLoginRegisterLoginRegisterRoutingModuleTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "LoginRegisterRoutingModule", function () {
      return LoginRegisterRoutingModule;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/router */
    "./node_modules/@angular/router/__ivy_ngcc__/fesm2015/router.js");
    /* harmony import */


    var _login_login_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ./login/login.component */
    "./src/app/login-register/login/login.component.ts");

    var routes = [{
      path: '',
      component: _login_login_component__WEBPACK_IMPORTED_MODULE_2__["LoginComponent"]
    }];

    var LoginRegisterRoutingModule = function LoginRegisterRoutingModule() {
      _classCallCheck(this, LoginRegisterRoutingModule);
    };

    LoginRegisterRoutingModule.ɵmod = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({
      type: LoginRegisterRoutingModule
    });
    LoginRegisterRoutingModule.ɵinj = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({
      factory: function LoginRegisterRoutingModule_Factory(t) {
        return new (t || LoginRegisterRoutingModule)();
      },
      imports: [[_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forChild(routes)], _angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
    });

    (function () {
      (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](LoginRegisterRoutingModule, {
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
      });
    })();
    /*@__PURE__*/


    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](LoginRegisterRoutingModule, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          imports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forChild(routes)],
          exports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
        }]
      }], null, null);
    })();
    /***/

  },

  /***/
  "./src/app/login-register/login-register.module.ts":
  /*!*********************************************************!*\
    !*** ./src/app/login-register/login-register.module.ts ***!
    \*********************************************************/

  /*! exports provided: LoginRegisterModule */

  /***/
  function srcAppLoginRegisterLoginRegisterModuleTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "LoginRegisterModule", function () {
      return LoginRegisterModule;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/common */
    "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/common.js");
    /* harmony import */


    var _login_login_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ./login/login.component */
    "./src/app/login-register/login/login.component.ts");
    /* harmony import */


    var _login_register_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! ./login-register-routing.module */
    "./src/app/login-register/login-register-routing.module.ts");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/__ivy_ngcc__/fesm2015/forms.js");

    var LoginRegisterModule = function LoginRegisterModule() {
      _classCallCheck(this, LoginRegisterModule);
    };

    LoginRegisterModule.ɵmod = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({
      type: LoginRegisterModule
    });
    LoginRegisterModule.ɵinj = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({
      factory: function LoginRegisterModule_Factory(t) {
        return new (t || LoginRegisterModule)();
      },
      imports: [[_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _login_register_routing_module__WEBPACK_IMPORTED_MODULE_3__["LoginRegisterRoutingModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormsModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"]]]
    });

    (function () {
      (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](LoginRegisterModule, {
        declarations: [_login_login_component__WEBPACK_IMPORTED_MODULE_2__["LoginComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _login_register_routing_module__WEBPACK_IMPORTED_MODULE_3__["LoginRegisterRoutingModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormsModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"]]
      });
    })();
    /*@__PURE__*/


    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](LoginRegisterModule, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          declarations: [_login_login_component__WEBPACK_IMPORTED_MODULE_2__["LoginComponent"]],
          imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _login_register_routing_module__WEBPACK_IMPORTED_MODULE_3__["LoginRegisterRoutingModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormsModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"]]
        }]
      }], null, null);
    })();
    /***/

  },

  /***/
  "./src/app/login-register/login/login.component.ts":
  /*!*********************************************************!*\
    !*** ./src/app/login-register/login/login.component.ts ***!
    \*********************************************************/

  /*! exports provided: LoginComponent */

  /***/
  function srcAppLoginRegisterLoginLoginComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "LoginComponent", function () {
      return LoginComponent;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/__ivy_ngcc__/fesm2015/forms.js");
    /* harmony import */


    var _services_auth_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ../services/auth.service */
    "./src/app/login-register/services/auth.service.ts");
    /* harmony import */


    var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @angular/common */
    "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/common.js");

    function LoginComponent_div_12_div_1_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Email address is required. ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function LoginComponent_div_12_div_2_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Email address is invalid. ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function LoginComponent_div_12_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, LoginComponent_div_12_div_1_Template, 2, 0, "div", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, LoginComponent_div_12_div_2_Template, 2, 0, "div", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r0.signinupFormValues.email.errors.required);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r0.signinupFormValues.email.errors.pattern);
      }
    }

    function LoginComponent_div_17_div_1_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Password is required. ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function LoginComponent_div_17_div_2_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Password should match contain at least one capital letter, one number and one special character. ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function LoginComponent_div_17_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, LoginComponent_div_17_div_1_Template, 2, 0, "div", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, LoginComponent_div_17_div_2_Template, 2, 0, "div", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r1.signinupFormValues.password.errors.required);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r1.signinupFormValues.password.errors.pattern);
      }
    }

    var _c0 = function _c0(a0) {
      return {
        "invalid-class": a0
      };
    };

    var LoginComponent = /*#__PURE__*/function () {
      function LoginComponent(authService) {
        _classCallCheck(this, LoginComponent);

        this.authService = authService;
        this.emailPattern = '^[a-zA-Z0-9.!#$%&*+/=?^_{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$';
        this.passwordPattern = '^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$';
      }

      _createClass(LoginComponent, [{
        key: "signinupFormValues",
        get: function get() {
          return this.signinupform.controls;
        }
      }, {
        key: "ngOnInit",
        value: function ngOnInit() {
          this.signinupform = new _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormGroup"]({
            email: new _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required, _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].pattern(this.emailPattern)]),
            password: new _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required, _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].pattern(this.passwordPattern)])
          });
        }
      }, {
        key: "signInUpMethod",
        value: function signInUpMethod(type) {
          this.authService.disableFlag = true;
          this.signinupFormValues.email.markAllAsTouched();
          this.signinupFormValues.password.markAllAsTouched();

          if (!this.signinupFormValues.email.invalid && !this.signinupFormValues.password.invalid) {
            if (type === 'SIGNIN') {
              this.authService.SignIn(this.signinupFormValues.email.value.toString(), this.signinupFormValues.password.value.toString());
            } else {
              this.authService.SignUp(this.signinupFormValues.email.value.toString(), this.signinupFormValues.password.value.toString());
            }
          }
        }
      }]);

      return LoginComponent;
    }();

    LoginComponent.ɵfac = function LoginComponent_Factory(t) {
      return new (t || LoginComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_auth_service__WEBPACK_IMPORTED_MODULE_2__["AuthService"]));
    };

    LoginComponent.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: LoginComponent,
      selectors: [["app-login"]],
      decls: 44,
      vars: 11,
      consts: [[1, "container"], [1, "form-signin", "text-center"], [3, "formGroup"], ["src", "../../../assets/team_icon.png", "alt", "", "width", "150", 1, "mb-2", 2, "margin-top", "65px"], [1, "h3", "mb-3", "fw-normal"], [1, "fw-bold"], [1, "form-floating"], ["type", "email", "id", "email", "formControlName", "email", "placeholder", "name@example.com", 1, "form-control", 3, "ngClass"], ["for", "floatingInput"], ["class", "invalid-field", 4, "ngIf"], ["type", "password", "id", "password", "formControlName", "password", "placeholder", "Password", 1, "form-control", 3, "ngClass"], ["for", "floatingPassword"], [1, "w-100", "btn", "btn-primary", 3, "disabled", "click"], [1, "mt-3", "text-muted"], [1, "btn-group"], [1, "icon-button", "facebook"], [1, "fa", "fa-facebook"], [1, "icon-button", "twitter"], [1, "fa", "fa-twitter"], [1, "icon-button", "google", 3, "click"], [1, "fa", "fa-google"], [1, "icon-button", "linkedin"], [1, "fa", "fa-linkedin"], [1, "icon-button", "instagram"], [1, "fa", "fa-instagram"], [1, "mt-2", "mb-3", "text-muted"], [1, "invalid-field"], [4, "ngIf"]],
      template: function LoginComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "form", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "img", 3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "h1", 4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](5, "The_Atlantians");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "p", 5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](7, "Sign in/up");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "div", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](9, "input", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](10, "label", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](11, "Email address");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](12, LoginComponent_div_12_Template, 3, 2, "div", 9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](13, "div", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](14, "input", 10);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](15, "label", 11);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](16, "Password");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](17, LoginComponent_div_17_Template, 3, 2, "div", 9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](18, "br");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](19, "button", 12);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function LoginComponent_Template_button_click_19_listener() {
            return ctx.signInUpMethod("SIGNIN");
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](20, "Sign in");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](21, "hr");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](22, "button", 12);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function LoginComponent_Template_button_click_22_listener() {
            return ctx.signInUpMethod("SIGNUP");
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](23, "Sign up");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](24, "p", 13);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](25, "Socials");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](26, "div", 14);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](27, "a", 15);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](28, "i", 16);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](29, "span");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](30, "a", 17);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](31, "i", 18);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](32, "span");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](33, "a", 19);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function LoginComponent_Template_a_click_33_listener() {
            return ctx.authService.GoogleAuth();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](34, "i", 20);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](35, "span");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](36, "a", 21);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](37, "i", 22);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](38, "span");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](39, "a", 23);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](40, "i", 24);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](41, "span");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](42, "p", 25);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](43, "\xA9 2021");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }

        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx.signinupform);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](7, _c0, ctx.signinupFormValues.email.errors && ctx.signinupFormValues.email.touched));

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.signinupFormValues.email.errors && ctx.signinupFormValues.email.touched);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](9, _c0, ctx.signinupFormValues.password.errors && ctx.signinupFormValues.password.touched));

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.signinupFormValues.password.errors && ctx.signinupFormValues.password.touched);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx.authService.disableFlag);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx.authService.disableFlag);
        }
      },
      directives: [_angular_forms__WEBPACK_IMPORTED_MODULE_1__["ɵangular_packages_forms_forms_y"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["NgControlStatusGroup"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormGroupDirective"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["DefaultValueAccessor"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["NgControlStatus"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormControlName"], _angular_common__WEBPACK_IMPORTED_MODULE_3__["NgClass"], _angular_common__WEBPACK_IMPORTED_MODULE_3__["NgIf"]],
      styles: [".form-signin[_ngcontent-%COMP%] {\r\n    width: 100%;\r\n    max-width: 330px;\r\n    padding: 15px;\r\n    margin: auto;\r\n}\r\nhtml[_ngcontent-%COMP%] {\r\n\tfont-size: 2.5em;\r\n}\r\nbody[_ngcontent-%COMP%] {\r\n\tbackground-color: #fff;\r\n\tpadding: 25px;\r\n\ttext-align: center;\r\n}\r\n\r\n.icon-button[_ngcontent-%COMP%] {\r\n\tbackground-color: white;\r\n\tborder-radius: 2.6rem;\r\n\tcursor: pointer;\r\n\tdisplay: inline-block;\r\n\tfont-size: 1.3rem;\r\n\theight: 2.6rem;\r\n\tline-height: 2.6rem;\r\n\tmargin: 0 5px;\r\n\tposition: relative;\r\n\ttext-align: center;\r\n\t-webkit-user-select: none;\r\n\t   -moz-user-select: none;\r\n\t        user-select: none;\r\n\twidth: 2.6rem;\r\n}\r\n\r\n.icon-button[_ngcontent-%COMP%]   span[_ngcontent-%COMP%] {\r\n\tborder-radius: 0;\r\n\tdisplay: block;\r\n\theight: 0;\r\n\tleft: 50%;\r\n\tmargin: 0;\r\n\tposition: absolute;\r\n\ttop: 50%;\r\n\ttransition: all 0.3s;\r\n\twidth: 0;\r\n}\r\n.icon-button[_ngcontent-%COMP%]:hover   span[_ngcontent-%COMP%] {\r\n\twidth: 2.6rem;\r\n\theight: 2.6rem;\r\n\tborder-radius: 2.6rem;\r\n\tmargin: -1.3rem;\r\n}\r\n\r\n.icon-button[_ngcontent-%COMP%]   i[_ngcontent-%COMP%] {\r\n\tbackground: none;\r\n\tcolor: white;\r\n\theight: 2.6rem;\r\n\tleft: 0;\r\n\tline-height: 2.6rem;\r\n\tposition: absolute;\r\n\ttop: 0;\r\n\ttransition: all 0.3s;\r\n\twidth: 2.6rem;\r\n\tz-index: 10;\r\n}\r\n.twitter[_ngcontent-%COMP%]   span[_ngcontent-%COMP%] {\r\n\tbackground-color: #4099ff;\r\n}\r\n.facebook[_ngcontent-%COMP%]   span[_ngcontent-%COMP%] {\r\n\tbackground-color: #3B5998;\r\n}\r\n.google[_ngcontent-%COMP%]   span[_ngcontent-%COMP%] {\r\n\tbackground-color: #db5a3c;\r\n}\r\n.linkedin[_ngcontent-%COMP%]   span[_ngcontent-%COMP%] {\r\n\tbackground-color: #1075af;\r\n}\r\n.instagram[_ngcontent-%COMP%]   span[_ngcontent-%COMP%] {\r\n\tbackground-color: #cb2027;\r\n}\r\n.icon-button[_ngcontent-%COMP%]   .fa-twitter[_ngcontent-%COMP%] {\r\n\tcolor: #4099ff;\r\n}\r\n.icon-button[_ngcontent-%COMP%]   .fa-facebook[_ngcontent-%COMP%] {\r\n\tcolor: #3B5998;\r\n}\r\n.icon-button[_ngcontent-%COMP%]   .fa-google[_ngcontent-%COMP%] {\r\n\tcolor: #db5a3c;\r\n}\r\n.icon-button[_ngcontent-%COMP%]   .fa-linkedin[_ngcontent-%COMP%] {\r\n\tcolor: #1075af;\r\n}\r\n.icon-button[_ngcontent-%COMP%]   .fa-instagram[_ngcontent-%COMP%] {\r\n\tcolor: #cb2027;\r\n}\r\n.icon-button[_ngcontent-%COMP%]:hover   .fa-twitter[_ngcontent-%COMP%], .icon-button[_ngcontent-%COMP%]:hover   .fa-facebook[_ngcontent-%COMP%], .icon-button[_ngcontent-%COMP%]:hover   .fa-google[_ngcontent-%COMP%], .icon-button[_ngcontent-%COMP%]:hover   .fa-instagram[_ngcontent-%COMP%], .icon-button[_ngcontent-%COMP%]:hover   .fa-linkedin[_ngcontent-%COMP%] {\r\n\tcolor: white;\r\n}\r\n@media all and (max-width: 680px) {\r\n  .icon-button[_ngcontent-%COMP%] {\r\n    border-radius: 1.6rem;\r\n    font-size: 0.8rem;\r\n    height: 1.6rem;\r\n    line-height: 1.6rem;\r\n    width: 1.6rem;\r\n  }\r\n\r\n  .icon-button[_ngcontent-%COMP%]:hover   span[_ngcontent-%COMP%] {\r\n    width: 1.6rem;\r\n    height: 1.6rem;\r\n    border-radius: 1.6rem;\r\n    margin: -0.8rem;\r\n  }\r\n\r\n  \r\n  .icon-button[_ngcontent-%COMP%]   i[_ngcontent-%COMP%] {\r\n\t  height: 1.6rem;\r\n\t  line-height: 1.6rem;\r\n\t  width: 1.6rem;\r\n  }\r\n  .pinterest[_ngcontent-%COMP%] {\r\n   display: none; \r\n  }\r\n\r\n}\r\n.invalid-class[_ngcontent-%COMP%] {\r\n\tborder: 1px solid red;\r\n}\r\n.invalid-field[_ngcontent-%COMP%] {\r\n    color: #dc3545 !important;\r\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbG9naW4tcmVnaXN0ZXIvbG9naW4vbG9naW4uY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtJQUNJLFdBQVc7SUFDWCxnQkFBZ0I7SUFDaEIsYUFBYTtJQUNiLFlBQVk7QUFDaEI7QUFDQTtDQUNDLGdCQUFnQjtBQUNqQjtBQUNBO0NBQ0Msc0JBQXNCO0NBQ3RCLGFBQWE7Q0FDYixrQkFBa0I7QUFDbkI7QUFFQSxZQUFZO0FBQ1o7Q0FDQyx1QkFBdUI7Q0FDdkIscUJBQXFCO0NBQ3JCLGVBQWU7Q0FDZixxQkFBcUI7Q0FDckIsaUJBQWlCO0NBQ2pCLGNBQWM7Q0FDZCxtQkFBbUI7Q0FDbkIsYUFBYTtDQUNiLGtCQUFrQjtDQUNsQixrQkFBa0I7Q0FDbEIseUJBQXlCO0lBQ3RCLHNCQUFzQjtTQUVqQixpQkFBaUI7Q0FDekIsYUFBYTtBQUNkO0FBRUEsV0FBVztBQUNYO0NBQ0MsZ0JBQWdCO0NBQ2hCLGNBQWM7Q0FDZCxTQUFTO0NBQ1QsU0FBUztDQUNULFNBQVM7Q0FDVCxrQkFBa0I7Q0FDbEIsUUFBUTtDQUlBLG9CQUFvQjtDQUM1QixRQUFRO0FBQ1Q7QUFDQTtDQUNDLGFBQWE7Q0FDYixjQUFjO0NBQ2QscUJBQXFCO0NBQ3JCLGVBQWU7QUFDaEI7QUFFQSxVQUFVO0FBQ1Y7Q0FDQyxnQkFBZ0I7Q0FDaEIsWUFBWTtDQUNaLGNBQWM7Q0FDZCxPQUFPO0NBQ1AsbUJBQW1CO0NBQ25CLGtCQUFrQjtDQUNsQixNQUFNO0NBSUUsb0JBQW9CO0NBQzVCLGFBQWE7Q0FDYixXQUFXO0FBQ1o7QUFFQTtDQUNDLHlCQUF5QjtBQUMxQjtBQUNBO0NBQ0MseUJBQXlCO0FBQzFCO0FBQ0E7Q0FDQyx5QkFBeUI7QUFDMUI7QUFDQTtDQUNDLHlCQUF5QjtBQUMxQjtBQUNBO0NBQ0MseUJBQXlCO0FBQzFCO0FBQ0E7Q0FDQyxjQUFjO0FBQ2Y7QUFDQTtDQUNDLGNBQWM7QUFDZjtBQUNBO0NBQ0MsY0FBYztBQUNmO0FBQ0E7Q0FDQyxjQUFjO0FBQ2Y7QUFDQTtDQUNDLGNBQWM7QUFDZjtBQUVBOzs7OztDQUtDLFlBQVk7QUFDYjtBQUVBO0VBQ0U7SUFDRSxxQkFBcUI7SUFDckIsaUJBQWlCO0lBQ2pCLGNBQWM7SUFDZCxtQkFBbUI7SUFDbkIsYUFBYTtFQUNmOztFQUVBO0lBQ0UsYUFBYTtJQUNiLGNBQWM7SUFDZCxxQkFBcUI7SUFDckIsZUFBZTtFQUNqQjs7RUFFQSxVQUFVO0VBQ1Y7R0FDQyxjQUFjO0dBQ2QsbUJBQW1CO0dBQ25CLGFBQWE7RUFDZDtFQUNBO0dBQ0MsYUFBYTtFQUNkOztBQUVGO0FBRUE7Q0FDQyxxQkFBcUI7QUFDdEI7QUFFQTtJQUNJLHlCQUF5QjtBQUM3QiIsImZpbGUiOiJzcmMvYXBwL2xvZ2luLXJlZ2lzdGVyL2xvZ2luL2xvZ2luLmNvbXBvbmVudC5jc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuZm9ybS1zaWduaW4ge1xyXG4gICAgd2lkdGg6IDEwMCU7XHJcbiAgICBtYXgtd2lkdGg6IDMzMHB4O1xyXG4gICAgcGFkZGluZzogMTVweDtcclxuICAgIG1hcmdpbjogYXV0bztcclxufVxyXG5odG1sIHtcclxuXHRmb250LXNpemU6IDIuNWVtO1xyXG59XHJcbmJvZHkge1xyXG5cdGJhY2tncm91bmQtY29sb3I6ICNmZmY7XHJcblx0cGFkZGluZzogMjVweDtcclxuXHR0ZXh0LWFsaWduOiBjZW50ZXI7XHJcbn1cclxuXHJcbi8qIFdyYXBwZXIgKi9cclxuLmljb24tYnV0dG9uIHtcclxuXHRiYWNrZ3JvdW5kLWNvbG9yOiB3aGl0ZTtcclxuXHRib3JkZXItcmFkaXVzOiAyLjZyZW07XHJcblx0Y3Vyc29yOiBwb2ludGVyO1xyXG5cdGRpc3BsYXk6IGlubGluZS1ibG9jaztcclxuXHRmb250LXNpemU6IDEuM3JlbTtcclxuXHRoZWlnaHQ6IDIuNnJlbTtcclxuXHRsaW5lLWhlaWdodDogMi42cmVtO1xyXG5cdG1hcmdpbjogMCA1cHg7XHJcblx0cG9zaXRpb246IHJlbGF0aXZlO1xyXG5cdHRleHQtYWxpZ246IGNlbnRlcjtcclxuXHQtd2Via2l0LXVzZXItc2VsZWN0OiBub25lO1xyXG5cdCAgIC1tb3otdXNlci1zZWxlY3Q6IG5vbmU7XHJcblx0ICAgIC1tcy11c2VyLXNlbGVjdDogbm9uZTtcclxuXHQgICAgICAgIHVzZXItc2VsZWN0OiBub25lO1xyXG5cdHdpZHRoOiAyLjZyZW07XHJcbn1cclxuXHJcbi8qIENpcmNsZSAqL1xyXG4uaWNvbi1idXR0b24gc3BhbiB7XHJcblx0Ym9yZGVyLXJhZGl1czogMDtcclxuXHRkaXNwbGF5OiBibG9jaztcclxuXHRoZWlnaHQ6IDA7XHJcblx0bGVmdDogNTAlO1xyXG5cdG1hcmdpbjogMDtcclxuXHRwb3NpdGlvbjogYWJzb2x1dGU7XHJcblx0dG9wOiA1MCU7XHJcblx0LXdlYmtpdC10cmFuc2l0aW9uOiBhbGwgMC4zcztcclxuXHQgICAtbW96LXRyYW5zaXRpb246IGFsbCAwLjNzO1xyXG5cdCAgICAgLW8tdHJhbnNpdGlvbjogYWxsIDAuM3M7XHJcblx0ICAgICAgICB0cmFuc2l0aW9uOiBhbGwgMC4zcztcclxuXHR3aWR0aDogMDtcclxufVxyXG4uaWNvbi1idXR0b246aG92ZXIgc3BhbiB7XHJcblx0d2lkdGg6IDIuNnJlbTtcclxuXHRoZWlnaHQ6IDIuNnJlbTtcclxuXHRib3JkZXItcmFkaXVzOiAyLjZyZW07XHJcblx0bWFyZ2luOiAtMS4zcmVtO1xyXG59XHJcblxyXG4vKiBJY29ucyAqL1xyXG4uaWNvbi1idXR0b24gaSB7XHJcblx0YmFja2dyb3VuZDogbm9uZTtcclxuXHRjb2xvcjogd2hpdGU7XHJcblx0aGVpZ2h0OiAyLjZyZW07XHJcblx0bGVmdDogMDtcclxuXHRsaW5lLWhlaWdodDogMi42cmVtO1xyXG5cdHBvc2l0aW9uOiBhYnNvbHV0ZTtcclxuXHR0b3A6IDA7XHJcblx0LXdlYmtpdC10cmFuc2l0aW9uOiBhbGwgMC4zcztcclxuXHQgICAtbW96LXRyYW5zaXRpb246IGFsbCAwLjNzO1xyXG5cdCAgICAgLW8tdHJhbnNpdGlvbjogYWxsIDAuM3M7XHJcblx0ICAgICAgICB0cmFuc2l0aW9uOiBhbGwgMC4zcztcclxuXHR3aWR0aDogMi42cmVtO1xyXG5cdHotaW5kZXg6IDEwO1xyXG59XHJcblxyXG4udHdpdHRlciBzcGFuIHtcclxuXHRiYWNrZ3JvdW5kLWNvbG9yOiAjNDA5OWZmO1xyXG59XHJcbi5mYWNlYm9vayBzcGFuIHtcclxuXHRiYWNrZ3JvdW5kLWNvbG9yOiAjM0I1OTk4O1xyXG59XHJcbi5nb29nbGUgc3BhbiB7XHJcblx0YmFja2dyb3VuZC1jb2xvcjogI2RiNWEzYztcclxufVxyXG4ubGlua2VkaW4gc3BhbiB7XHJcblx0YmFja2dyb3VuZC1jb2xvcjogIzEwNzVhZjtcclxufVxyXG4uaW5zdGFncmFtIHNwYW4ge1xyXG5cdGJhY2tncm91bmQtY29sb3I6ICNjYjIwMjc7XHJcbn1cclxuLmljb24tYnV0dG9uIC5mYS10d2l0dGVyIHtcclxuXHRjb2xvcjogIzQwOTlmZjtcclxufVxyXG4uaWNvbi1idXR0b24gLmZhLWZhY2Vib29rIHtcclxuXHRjb2xvcjogIzNCNTk5ODtcclxufVxyXG4uaWNvbi1idXR0b24gLmZhLWdvb2dsZSB7XHJcblx0Y29sb3I6ICNkYjVhM2M7XHJcbn1cclxuLmljb24tYnV0dG9uIC5mYS1saW5rZWRpbiB7XHJcblx0Y29sb3I6ICMxMDc1YWY7XHJcbn1cclxuLmljb24tYnV0dG9uIC5mYS1pbnN0YWdyYW0ge1xyXG5cdGNvbG9yOiAjY2IyMDI3O1xyXG59XHJcblxyXG4uaWNvbi1idXR0b246aG92ZXIgLmZhLXR3aXR0ZXIsXHJcbi5pY29uLWJ1dHRvbjpob3ZlciAuZmEtZmFjZWJvb2ssXHJcbi5pY29uLWJ1dHRvbjpob3ZlciAuZmEtZ29vZ2xlLFxyXG4uaWNvbi1idXR0b246aG92ZXIgLmZhLWluc3RhZ3JhbSxcclxuLmljb24tYnV0dG9uOmhvdmVyIC5mYS1saW5rZWRpbiB7XHJcblx0Y29sb3I6IHdoaXRlO1xyXG59XHJcblxyXG5AbWVkaWEgYWxsIGFuZCAobWF4LXdpZHRoOiA2ODBweCkge1xyXG4gIC5pY29uLWJ1dHRvbiB7XHJcbiAgICBib3JkZXItcmFkaXVzOiAxLjZyZW07XHJcbiAgICBmb250LXNpemU6IDAuOHJlbTtcclxuICAgIGhlaWdodDogMS42cmVtO1xyXG4gICAgbGluZS1oZWlnaHQ6IDEuNnJlbTtcclxuICAgIHdpZHRoOiAxLjZyZW07XHJcbiAgfVxyXG5cclxuICAuaWNvbi1idXR0b246aG92ZXIgc3BhbiB7XHJcbiAgICB3aWR0aDogMS42cmVtO1xyXG4gICAgaGVpZ2h0OiAxLjZyZW07XHJcbiAgICBib3JkZXItcmFkaXVzOiAxLjZyZW07XHJcbiAgICBtYXJnaW46IC0wLjhyZW07XHJcbiAgfVxyXG5cclxuICAvKiBJY29ucyAqL1xyXG4gIC5pY29uLWJ1dHRvbiBpIHtcclxuXHQgIGhlaWdodDogMS42cmVtO1xyXG5cdCAgbGluZS1oZWlnaHQ6IDEuNnJlbTtcclxuXHQgIHdpZHRoOiAxLjZyZW07XHJcbiAgfVxyXG4gIC5waW50ZXJlc3Qge1xyXG4gICBkaXNwbGF5OiBub25lOyBcclxuICB9XHJcblxyXG59XHJcblxyXG4uaW52YWxpZC1jbGFzcyB7XHJcblx0Ym9yZGVyOiAxcHggc29saWQgcmVkO1xyXG59XHJcblxyXG4uaW52YWxpZC1maWVsZCB7XHJcbiAgICBjb2xvcjogI2RjMzU0NSAhaW1wb3J0YW50O1xyXG59Il19 */"]
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](LoginComponent, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'app-login',
          templateUrl: './login.component.html',
          styleUrls: ['./login.component.css']
        }]
      }], function () {
        return [{
          type: _services_auth_service__WEBPACK_IMPORTED_MODULE_2__["AuthService"]
        }];
      }, null);
    })();
    /***/

  }
}]);
//# sourceMappingURL=login-register-login-register-module-es5.js.map