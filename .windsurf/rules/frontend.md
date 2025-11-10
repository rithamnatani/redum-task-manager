<!-- trunk-ignore-all(prettier) -->
---
trigger: model_decision
description: when working on frontend
---

CoreModule, SharedModule, FeatureModule pattern required
State management with RxJS BehaviorSubjects only (NO NgRx)
Angular Reactive Forms mandatory for all user input.

Using  "dependencies": {
    "@angular/cdk": "^20.2.12",
    "@angular/common": "^20.3.0",
    "@angular/compiler": "^20.3.0",
    "@angular/core": "^20.3.0",
    "@angular/forms": "^20.3.0",
    "@angular/material": "^20.2.12",
    "@angular/platform-browser": "^20.3.0",
    "@angular/router": "^20.3.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.15.0"
  },

Make sure to not use deprecated code.
