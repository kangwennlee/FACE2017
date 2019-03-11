import { Face2Component } from './face2/face2.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule, PreloadAllModules } from '@angular/router';

const appRoutes: Routes = [ 
 { path: '', component: Face2Component },
 { path: 'face2', component: Face2Component },
];

@NgModule({
 imports: [RouterModule.forRoot(appRoutes, {preloadingStrategy: PreloadAllModules})],
 exports: [RouterModule]
})
export class AppRoutingModule { }
