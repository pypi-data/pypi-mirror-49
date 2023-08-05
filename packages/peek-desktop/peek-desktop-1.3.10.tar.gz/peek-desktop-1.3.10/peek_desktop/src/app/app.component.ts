import {Component} from "@angular/core";
import {VortexService, VortexStatusService} from "@synerty/vortexjs";
import {OnInit} from "@angular/core";
import {DeviceStatusService} from "@peek/peek_core_device"

@Component({
    selector: "peek-main-app",
    templateUrl: "app.component.dweb.html",
    styleUrls: ["app.component.dweb.scss"],
    moduleId: module.id
})
export class AppComponent implements OnInit {

    constructor(private vortexService: VortexService,
                private vortexStatusService: VortexStatusService,
                private deviceStatusService:DeviceStatusService) {

    }

    ngOnInit() {
        this.vortexService.reconnect();
    }

    showLoading():boolean {
        return this.deviceStatusService.isLoading;
    }

}

