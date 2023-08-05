import {Injectable, NgZone} from "@angular/core";
import {
    TupleActionPushNameService,
    TupleActionPushOfflineService,
    TupleActionPushOfflineSingletonService,
    TupleDataObservableNameService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService,
    TupleStorageFactoryService,
    VortexService,
    VortexStatusService
} from "@synerty/vortexjs";

import {
    diagramGenericMenuActionProcessorName,
    diagramGenericMenuFilt,
    diagramGenericMenuObservableName,
    diagramGenericMenuTupleOfflineServiceName
} from "../PluginNames";


@Injectable()
export class PrivateGenericTupleService  {

    public tupleOfflineAction: TupleActionPushOfflineService;
    public tupleDataOfflineObserver: TupleDataOfflineObserverService;


    constructor(tupleActionSingletonService: TupleActionPushOfflineSingletonService,
                vortexService: VortexService,
                vortexStatusService: VortexStatusService,
                storageFactory: TupleStorageFactoryService) {


        let tupleDataObservableName = new TupleDataObservableNameService(
            diagramGenericMenuObservableName, diagramGenericMenuFilt);

        let storageName = new TupleOfflineStorageNameService(
            diagramGenericMenuTupleOfflineServiceName);

        let tupleActionName = new TupleActionPushNameService(
            diagramGenericMenuActionProcessorName, diagramGenericMenuFilt);

        let tupleOfflineStorageService = new TupleOfflineStorageService(
            storageFactory, storageName);

        this.tupleDataOfflineObserver = new TupleDataOfflineObserverService(
            vortexService,
            vortexStatusService,
            tupleDataObservableName,
            tupleOfflineStorageService);


        this.tupleOfflineAction = new TupleActionPushOfflineService(
            tupleActionName,
            vortexService,
            vortexStatusService,
            tupleActionSingletonService);

    }


}