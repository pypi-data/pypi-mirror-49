(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{"7yFK":function(t,e){t.exports='<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">\n\n<table style="width: 70%;">\n  <td class="mat-app-background basic-container" style="width: 30%">\n  <mat-tree [dataSource]="dataSource" [treeControl]="treeControl">\n    \x3c!-- This is the tree node template for leaf nodes --\x3e\n    <mat-tree-node *matTreeNodeDef="let node" matTreeNodePadding>\n      \x3c!-- use a disabled button to provide padding for tree leaf --\x3e\n      <button mat-icon-button mat-button class="mat-icon-button" (click)="node_click(node)"></button>\n      {{node.name}}\n    </mat-tree-node>\n     This is the tree node template for expandable nodes\n    <mat-tree-node *matTreeNodeDef="let node;when: hasChild" matTreeNodePadding>\n      <button mat-icon-button matTreeNodeToggle\n              [attr.aria-label]="\'toggle \' + node.name" class="mat-icon-button">\n        <mat-icon class="mat-icon-rtl-mirror">\n          {{treeControl.isExpanded(node) ? \'expand_more\' : \'chevron_right\'}}\n        </mat-icon>\n      </button>\n      {{node.name}}\n     </mat-tree-node>\n    </mat-tree>\n  </td>\n\n  <td style="width: 70%">\n    <div id="codeholder">\n\n    </div>\n\n  </td>\n</table>\n'},"8kgY":function(t,e){t.exports='<div class="mat-elevation-z8">\n    <table mat-table [dataSource]="dataSource" matSort>\n\n        <ng-container matColumnDef="id">\n            <th mat-header-cell *matHeaderCellDef  style="width: 18px" mat-sort-header> Id</th>\n            <td mat-cell *matCellDef="let element" style="width: 18px">\n                {{element.id}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="name">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Name</th>\n            <td mat-cell *matCellDef="let element">\n                <a class="col-1-4" routerLink="/dags/dag-detail/{{element.id}}">\n                    {{element.name}}\n                </a>\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="task_count">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header  style="width: 18px"> Tasks</th>\n            <td mat-cell *matCellDef="let element"  style="width: 18px">\n                {{element.task_count}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="created">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Created</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.created| date:"MM.dd H:mm"}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="started">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Started</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.started| date:"MM.dd H:mm"}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="last_activity">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Last activity</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.last_activity| date:"MM.dd H:mm"}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="duration">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Duration</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.duration}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="img_size">\n            <th mat-header-cell *matHeaderCellDef> Image size</th>\n            <td mat-cell *matCellDef="let element" style="width: 50px">\n                {{size(element.img_size)}}\n                <mat-icon svgIcon="remove" matTooltip="Remove" (click)="remove_imgs(element)"></mat-icon>\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="file_size">\n            <th mat-header-cell *matHeaderCellDef> File size</th>\n            <td mat-cell *matCellDef="let element"  style="width: 50px">\n                {{size(element.file_size)}}\n                <mat-icon svgIcon="remove" matTooltip="Remove" (click)="remove_files(element)"\n                [class.transparent]="has_unfinished(element)"></mat-icon>\n            </td>\n        </ng-container>\n\n\n        <ng-container matColumnDef="task_status">\n            <th mat-header-cell *matHeaderCellDef style="text-align: center"> Task status</th>\n            <td mat-cell *matCellDef="let element">\n                <svg height="40" width="220px" style="display: block;">\n                    <g matTooltip="{{status.name}}" [attr.transform]="\'translate(\'+(16+i*30).toString()+\',\'+\'20)\'"\n                       *ngFor="let status of element.task_statuses; let i = index">\n\n                        <text fill="black" text-anchor="middle" vertical-align="middle"\n                              font-size="10" y="3">{{status.count > 0 ? status.count : \'\'}}</text>\n\n                        <circle [attr.stroke-width]="status.count>0?2:1" (click)="status_click(element, status)"\n                                [attr.stroke]="color_for_task_status(status.name, status.count)"\n                                fill-opacity="0" r="12.5" style="cursor: pointer; opacity: 1;"></circle>\n                    </g>\n\n                </svg>\n\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="links">\n            <th mat-header-cell *matHeaderCellDef style="text-align: center; width: 14%;"> Links</th>\n            <td mat-cell *matCellDef="let element" style="padding-left: 1%;min-width: 120px">\n                <mat-icon svgIcon="config" matTooltip="Config"\n                          routerLink="/dags/dag-detail/{{element.id}}/config"></mat-icon>\n                <mat-icon svgIcon="code" matTooltip="Code" routerLink="/dags/dag-detail/{{element.id}}/code"></mat-icon>\n                <mat-icon svgIcon="graph" matTooltip="Graph" routerLink="/dags/dag-detail/{{element.id}}/graph"></mat-icon>\n                <mat-icon svgIcon="stop" matTooltip="Stop" (click)="stop(element)"\n                          [class.transparent]="!has_unfinished(element)"></mat-icon>\n                <mat-icon svgIcon="remove" matTooltip="Remove" (click)="remove(element)"></mat-icon>\n                <mat-icon svgIcon="report" matTooltip="Report" (click)="toogle_report(element)" *ngIf="report"\n                          [class.transparent]="!element.report_full"></mat-icon>\n            </td>\n        </ng-container>\n\n        <tr mat-header-row *matHeaderRowDef="displayed_columns"></tr>\n        <tr mat-row *matRowDef="let row; columns: displayed_columns;"></tr>\n    </table>\n\n\n</div>\n\n\n<nav>\n  <a routerLink="./" routerLinkActive="active">Tasks</a>\n  <a routerLink="./config" routerLinkActive="active">Config</a>\n  <a routerLink="./code" routerLinkActive="active">Code</a>\n  <a routerLink="./graph" routerLinkActive="active">Graph</a>\n</nav>\n\n<router-outlet (activate)="onActivate($event)"></router-outlet>'},B6gx:function(t,e){t.exports="#mynetwork {\n    border: 1px solid black;\n    background: white;\n    display: inline-block;\n    width: 100%;\n    height: 600px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvZGFnL2RhZy1kZXRhaWwvZ3JhcGgvZ3JhcGguY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtJQUNJLHVCQUF1QjtJQUN2QixpQkFBaUI7SUFDakIscUJBQXFCO0lBQ3JCLFdBQVc7SUFDWCxhQUFhO0FBQ2pCIiwiZmlsZSI6InNyYy9hcHAvZGFnL2RhZy1kZXRhaWwvZ3JhcGgvZ3JhcGguY29tcG9uZW50LmNzcyIsInNvdXJjZXNDb250ZW50IjpbIiNteW5ldHdvcmsge1xuICAgIGJvcmRlcjogMXB4IHNvbGlkIGJsYWNrO1xuICAgIGJhY2tncm91bmQ6IHdoaXRlO1xuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgICB3aWR0aDogMTAwJTtcbiAgICBoZWlnaHQ6IDYwMHB4O1xufSJdfQ== */"},KkV2:function(t,e){t.exports='<div id="mynetwork"></div>'},LlcR:function(t,e,n){"use strict";n.r(e);var a=n("mrSG"),o=n("CcnG"),r=n("ZYCi"),l=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return a.c(e,t),e.prototype.get_filter=function(){var e=t.prototype.get_filter.call(this);return e.id=parseInt(this.route.snapshot.paramMap.get("id")),e},e.prototype.onActivate=function(t){t.task=parseInt(this.route.snapshot.paramMap.get("id"))},e=a.b([Object(o.n)({selector:"app-task-detail",template:n("aTOI"),styles:[n("g8K3")]})],e)}(n("wXNr").a),i=n("WpE8"),s=n("dK7+"),c=n("Ip0R"),d=n("J12g"),m=n("SMsm"),p=n("ZYjt"),u=n("OdHV"),h=n("OBdK"),g=n("DK97"),f=n("24n0"),v=n("F/XL"),y=function(){function t(t,e,n,a,o,r,l){var i=this;this.service=t,this.location=e,this.router=n,this.route=a,this.message_service=l,this.flat_node_map=new Map,this.transformer=function(t,e){var n={expandable:!!t.children&&t.children.length>0,name:t.name,level:e,content:t};if(t.id in i.flat_node_map){var a=i.flat_node_map[t.id];for(var o in n)n[o]!=a[o]&&Object.defineProperty(a,o,{value:n[o]});return a}return i.flat_node_map[t.id]=n,n},this.get_children=function(t){return Object(v.a)(t.children)},this.treeControl=new h.i(function(t){return t.level},function(t){return t.expandable}),this.treeFlattener=new d.b(this.transformer,function(t){return t.level},function(t){return t.expandable},this.get_children),this.dataSource=new d.a(this.treeControl,this.treeFlattener),this.hasChild=function(t,e){return e.expandable}}return t.prototype.load=function(){var t=this;this.service.steps(this.task).subscribe(function(e){t.dataSource.data=e,t.treeControl.expandAll()})},t.prototype.ngOnInit=function(){var t=this;this.load(),this.interval=setInterval(function(){return t.load()},3e3)},t.prototype.node_click=function(t){},t.prototype.status_color=function(t){switch(t){case"in_progress":return"green";case"failed":return"red";case"stopped":return"orange";case"successed":return"green";default:throw new TypeError("unknown status: "+t)}},t.prototype.color_for_log_status=function(t,e){return e>0?f.a.log_colors[t]:"gainsboro"},t.prototype.status_click=function(t,e){t.content.init_level=e},t.prototype.ngOnDestroy=function(){clearInterval(this.interval)},t=a.b([Object(o.n)({selector:"app-step",template:n("T1WG"),styles:[n("c4K0")]}),a.d("design:paramtypes",[g.a,c.f,r.b,r.a,m.b,p.c,u.a])],t)}(),b=[{path:"",component:l,children:[{path:"report",component:s.a},{path:"step",component:y},{path:"",component:i.a}]}],C=function(){function t(){}return t=a.b([Object(o.L)({imports:[r.c.forChild(b)],exports:[r.c]})],t)}(),k=n("d2mR");n.d(e,"TaskDetailModule",function(){return w});var w=function(){function t(){}return t=a.b([Object(o.L)({imports:[C,k.a],declarations:[l,y]})],t)}()},MPo4:function(t,e){t.exports=".mat-tree-node { min-height: 20px }\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvZGFnL2RhZy1kZXRhaWwvY29kZS9jb2RlLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUEsaUJBQWlCLGlCQUFpQiIsImZpbGUiOiJzcmMvYXBwL2RhZy9kYWctZGV0YWlsL2NvZGUvY29kZS5jb21wb25lbnQuY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLm1hdC10cmVlLW5vZGUgeyBtaW4taGVpZ2h0OiAyMHB4IH0iXX0= */"},T1WG:function(t,e){t.exports='<mat-tree [dataSource]="dataSource" [treeControl]="treeControl">\n    \x3c!-- This is the tree node template for leaf nodes --\x3e\n    <mat-tree-node *matTreeNodeDef="let node" matTreeNodePadding>\n        \x3c!-- use a disabled button to provide padding for tree leaf --\x3e\n        <button mat-icon-button mat-button class="mat-icon-button" (click)="node_click(node)"></button>\n\n        <mat-accordion>\n            <mat-expansion-panel  (opened)="node.opened = true" (closed)="node.opened = false">\n                <mat-expansion-panel-header>\n                    <mat-panel-title>\n                        <span [style.margin]="\'auto\'">{{node.name}}</span>\n                    </mat-panel-title>\n                    <mat-panel-description>\n                        <span [style.color]="status_color(node.content.status)" [style.margin]="\'auto\'">{{node.content.status}}</span>\n\n                        <span style="padding: 10px">{{node.content.duration}}</span>\n\n                        <svg height="40" width="220px" style="display: block;">\n                            <g matTooltip="{{status.name}}"\n                               [attr.transform]="\'translate(\'+(16+i*30).toString()+\',\'+\'20)\'"\n                               *ngFor="let status of node.content.log_statuses; let i = index">\n\n                                <text fill="black" text-anchor="middle" vertical-align="middle"\n                                      font-size="10" y="3">{{status.count > 0 ? status.count : \'\'}}</text>\n\n                                <circle [attr.stroke-width]="status.count>0?2:1" (click)="status_click(node, status.name)"\n                                        [attr.stroke]="color_for_log_status(status.name, status.count)"\n                                        fill-opacity="0" r="12.5" style="cursor: pointer; opacity: 1;"></circle>\n                            </g>\n\n                        </svg>\n\n                    </mat-panel-description>\n                </mat-expansion-panel-header>\n\n                <app-log *ngIf="node.opened" [step]="node.content.id" [init_level]="node.content.init_level"></app-log>\n\n            </mat-expansion-panel>\n        </mat-accordion>\n\n\n    </mat-tree-node>\n    This is the tree node template for expandable nodes\n    <mat-tree-node *matTreeNodeDef="let node;when: hasChild" matTreeNodePadding>\n        <button mat-icon-button matTreeNodeToggle\n                [attr.aria-label]="\'toggle \' + node.name" class="mat-icon-button">\n            <mat-icon class="mat-icon-rtl-mirror">\n\n            </mat-icon>\n        </button>\n\n            <mat-accordion>\n            <mat-expansion-panel  (opened)="node.opened = true" (closed)="node.opened = false">\n                <mat-expansion-panel-header>\n                    <mat-panel-title>\n                        <span [style.margin]="\'auto\'">{{node.name}}</span>\n                    </mat-panel-title>\n                    <mat-panel-description>\n                        <span [style.color]="status_color(node.content.status)" [style.margin]="\'auto\'">{{node.content.status}}</span>\n\n                        <span style="padding: 10px">{{node.content.duration}}</span>\n\n                        <svg height="40" width="220px" style="display: block;">\n                            <g matTooltip="{{status.name}}"\n                               [attr.transform]="\'translate(\'+(16+i*30).toString()+\',\'+\'20)\'"\n                               *ngFor="let status of node.content.log_statuses; let i = index">\n\n                                <text fill="black" text-anchor="middle" vertical-align="middle"\n                                      font-size="10" y="3">{{status.count > 0 ? status.count : \'\'}}</text>\n\n                                <circle [attr.stroke-width]="status.count>0?2:1" (click)="status_click(node, status.name)"\n                                        [attr.stroke]="color_for_log_status(status.name, status.count)"\n                                        fill-opacity="0" r="12.5" style="cursor: pointer; opacity: 1;"></circle>\n                            </g>\n\n                        </svg>\n\n                    </mat-panel-description>\n                </mat-expansion-panel-header>\n\n                <app-log *ngIf="node.opened" [step]="node.content.id" [init_level]="node.content.init_level"></app-log>\n\n            </mat-expansion-panel>\n        </mat-accordion>\n\n    </mat-tree-node>\n</mat-tree>'},TBLF:function(t,e){t.exports='<div id="codeholder">\n\n</div>\n'},"Xy/L":function(t,e,n){"use strict";n.r(e);var a=n("mrSG"),o=n("CcnG"),r=n("OBdK"),l=n("J12g"),i=n("xMyE"),s=n("9Z1F"),c=n("24n0"),d=n("2G9v"),m=function(t){function e(){var e=null!==t&&t.apply(this,arguments)||this;return e.url=""+c.a.API_ENDPOINT,e}return a.c(e,t),e.prototype.get_config=function(t){var e=this;return this.http.post(this.url+"config",t).pipe(Object(i.a)(function(t){return e.log("fetched config")}),Object(s.a)(this.handleError("config",new d.e)))},e.prototype.get_code=function(t){var e=this;return this.http.post(this.url+"code",t).pipe(Object(i.a)(function(t){return e.log("fetched code")}),Object(s.a)(this.handleError("config",[])))},e.prototype.get_graph=function(t){var e=this;return this.http.post(this.url+"graph",t).pipe(Object(i.a)(function(t){return e.log("fetched graph")}),Object(s.a)(this.handleError("graph",new d.f)))},e=a.b([Object(o.D)({providedIn:"root"})],e)}(n("Bqtk").a),p=n("ZYCi"),u=n("OdHV"),h=n("9VKz"),g=function(){function t(t,e,n,a){this.service=t,this.route=e,this.message_service=n,this.resource_service=a,this.transformer=function(t,e){return{expandable:!!t.children&&t.children.length>0,name:t.name,level:e,content:t.content}},this.treeControl=new r.i(function(t){return t.level},function(t){return t.expandable}),this.treeFlattener=new l.b(this.transformer,function(t){return t.level},function(t){return t.expandable},function(t){return t.children}),this.dataSource=new l.a(this.treeControl,this.treeFlattener),this.hasChild=function(t,e){return e.expandable}}return t.prototype.ngAfterViewInit=function(){var t=this;this.service.get_code(this.dag).subscribe(function(e){t.dataSource.data=e}),this.resource_service.load("prettify","prettify-yaml","prettify-css")},t.prototype.prettify_lang=function(t){switch(t){case"py":return"lang-py";case"yaml":case"yml":return"lang-yaml";case"json":return"lang-json";default:return""}},t.prototype.node_click=function(t){var e=document.createElement("pre");e.textContent=t.content;var n=-1!=t.name.indexOf(".")?t.name.split(".")[1].toLowerCase():"";e.className="prettyprint linenums "+this.prettify_lang(n);var a=document.getElementById("codeholder");a.innerHTML="",a.appendChild(e),window.PR.prettyPrint()},t=a.b([Object(o.n)({selector:"app-code",template:n("7yFK"),styles:[n("MPo4")]}),a.d("design:paramtypes",[m,p.a,u.a,h.a])],t)}(),f=function(){function t(t,e,n){this.message_service=t,this.service=e,this.resource_service=n}return t.prototype.ngAfterViewInit=function(){var t=this;this.resource_service.load("prettify","prettify-yaml","prettify-css").then(function(){t.service.get_config(t.dag).subscribe(function(t){var e=document.createElement("pre");e.textContent=t.data,e.className="prettyprint linenums lang-yaml",document.getElementById("codeholder").appendChild(e),window.PR.prettyPrint()})})},t=a.b([Object(o.n)({selector:"app-config",template:n("TBLF"),styles:[n("p8w6")]}),a.d("design:paramtypes",[u.a,m,h.a])],t)}(),v=function(){function t(t,e,n,a,o){this.message_service=t,this.route=e,this.service=n,this.resource_service=a,this.router=o}return t.prototype.ngAfterViewInit=function(){var t=this;this.load_network(),this.interval=setInterval(function(){return t.load_network()},3e3)},t.prototype.load_network=function(){var t=this,e=this;this.resource_service.load("vis.min.js","vis.min.css").then(function(n){t.service.get_graph(t.dag).subscribe(function(n){n.nodes.forEach(function(t){return t.color=c.a.status_colors[t.status]}),n.edges.forEach(function(t){return t.color=c.a.status_colors[t.status]});var a=window.vis,o=new a.DataSet(n.nodes),r=new a.DataSet(n.edges),l=document.getElementById("mynetwork");if(t.data){for(var i=0,s=n.nodes;i<s.length;i++){var d=s[i];t.data.nodes.update(d)}for(var m=0,p=n.edges;m<p.length;m++){d=p[m];t.data.nodes.update(d)}}else{t.data={nodes:o,edges:r};new a.Network(l,t.data,{layout:{hierarchical:{direction:"LR",sortMethod:"directed"}},edges:{arrows:"to"}}).on("doubleClick",function(t){var n=t.nodes,a=o.get(n);e.router.navigate(["/tasks/task-detail/"+a[0].id+"/log"])})}})}).catch(function(e){return t.message_service.add(e)})},t.prototype.ngOnDestroy=function(){clearInterval(this.interval)},t=a.b([Object(o.n)({selector:"app-graph",template:n("KkV2"),styles:[n("B6gx")]}),a.d("design:paramtypes",[u.a,p.a,m,h.a,p.b])],t)}(),y=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return a.c(e,t),e.prototype.get_filter=function(){var e=t.prototype.get_filter.call(this);return e.id=parseInt(this.route.snapshot.paramMap.get("id")),e},e.prototype.onActivate=function(t){t.dag=parseInt(this.route.snapshot.paramMap.get("id"))},e=a.b([Object(o.n)({selector:"app-dag-detail",template:n("8kgY"),styles:[n("UHhX")]})],e)}(n("ujTt").a),b=n("wXNr"),C=[{path:"",component:y,children:[{path:"code",component:g},{path:"config",component:f},{path:"graph",component:v},{path:"",component:b.a}]}],k=function(){function t(){}return t=a.b([Object(o.L)({imports:[p.c.forChild(C)],exports:[p.c]})],t)}(),w=n("d2mR");n.d(e,"DagDetailModule",function(){return _});var _=function(){function t(){}return t=a.b([Object(o.L)({imports:[k,w.a],declarations:[g,f,v,y]})],t)}()},aTOI:function(t,e){t.exports='<div class="mat-elevation-z8">\n    <table mat-table [dataSource]="dataSource" matSort>\n\n        <ng-container matColumnDef="id">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header style="width: 3%"> Id</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.id}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="name">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header style="min-width: 100px"> Name</th>\n            <td mat-cell *matCellDef="let element">\n                <a class="col-1-4" routerLink="/tasks/task-detail/{{element.id}}">\n                    {{element.name}}\n                </a>\n\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="created">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Created</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.dag_rel.created| date:"MM.dd H:mm"}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="started">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Started</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.started| date:"MM.dd H:mm"}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="last_activity">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Last activity</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.last_activity| date:"MM.dd H:mm"}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="duration">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Duration</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.duration}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="status">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Status</th>\n            <td mat-cell *matCellDef="let element" [style.color]="status_color(element.status)">\n                {{element.status}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="executor">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header> Executor</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.executor}}\n            </td>\n        </ng-container>\n\n\n        <ng-container matColumnDef="dag">\n            <th mat-header-cell *matHeaderCellDef> Dag</th>\n            <td mat-cell *matCellDef="let element">\n                <a class="col-1-4" routerLink="/dags/dag-detail/{{element.dag_rel.id}}">\n                    {{element.dag_rel.name}}({{element.dag_rel.id}})\n                </a>\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="computer">\n            <th mat-header-cell *matHeaderCellDef> Computer/assigned</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.computer}}/{{element.computer_assigned}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="requirements">\n            <th mat-header-cell *matHeaderCellDef style="width: 100px"> Requirements</th>\n            <td mat-cell *matCellDef="let element">\n                <svg height="40" width="100px" style="display: block;">\n                    <g matTooltip="gpu" transform="translate(20, 20)">\n\n                        <text fill="black" text-anchor="middle" vertical-align="middle" font-size="10"\n                              y="3">{{element.gpu > 0 ? element.gpu : \'\'}}</text>\n\n                        <circle [attr.stroke-width]="element.gpu>0?2:1"\n                                [attr.stroke]="element.gpu>0?\'green\':\'gainsboro\'" fill-opacity="0" r="12.5"></circle>\n                    </g>\n\n                    <g matTooltip="cpu" transform="translate(50, 20)">\n\n                        <text fill="black" text-anchor="middle" vertical-align="middle" font-size="10"\n                              y="3">{{element.cpu > 1 ? element.cpu : \'\'}}</text>\n\n                        <circle [attr.stroke-width]="element.cpu>1?2:1"\n                                [attr.stroke]="element.cpu>1?\'OrangeRed\':\'gainsboro\'" fill-opacity="0" r="12.5"></circle>\n                    </g>\n\n                    <g matTooltip="memory" transform="translate(80, 20)">\n\n                        <text fill="black" text-anchor="middle" vertical-align="middle" font-size="10"\n                              y="3">{{element.memory > 0.1 ? element.memory : \'\'}}</text>\n\n                        <circle [attr.stroke-width]="element.memory>0.1?2:1"\n                                [attr.stroke]="element.memory>0.1?\'blue\':\'gainsboro\'" fill-opacity="0" r="12.5"></circle>\n                    </g>\n                </svg>\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef="steps">\n            <th mat-header-cell *matHeaderCellDef style="width: 60px"> Steps</th>\n            <td mat-cell *matCellDef="let element">\n                {{element.current_step}}<span *ngIf="element.steps>0">/{{element.steps}}</span>\n            </td>\n        </ng-container>\n\n\n        <ng-container matColumnDef="links">\n            <th mat-header-cell *matHeaderCellDef style="width: 60px"> Links</th>\n            <td mat-cell *matCellDef="let element" style="min-width: 100px">\n                <mat-icon svgIcon="stop" matTooltip="Stop" (click)="stop(element)" [class.transparent]="!unfinished(element)"></mat-icon>\n                <mat-icon svgIcon="report" matTooltip="Report" (click)="toogle_report(element)" *ngIf="report"\n                          [class.transparent]="!element.report_full"></mat-icon>\n            </td>\n        </ng-container>\n\n        <tr mat-header-row *matHeaderRowDef="displayed_columns"></tr>\n        <tr mat-row *matRowDef="let row; columns: displayed_columns;"></tr>\n    </table>\n\n</div>\n\n\n<nav>\n    <a routerLink="./" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: true }">Logs</a>\n    <a routerLink="./step" routerLinkActive="active">Steps</a>\n    <a routerLink="./report" routerLinkActive="active">Reports</a>\n</nav>\n\n<router-outlet (activate)="onActivate($event)"></router-outlet>'},c4K0:function(t,e){t.exports="\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Rhc2svdGFzay1kZXRhaWwvc3RlcC9zdGVwLmNvbXBvbmVudC5jc3MifQ== */"},p8w6:function(t,e){t.exports="\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL2RhZy9kYWctZGV0YWlsL2NvbmZpZy9jb25maWcuY29tcG9uZW50LmNzcyJ9 */"}}]);
//# sourceMappingURL=common.js.map