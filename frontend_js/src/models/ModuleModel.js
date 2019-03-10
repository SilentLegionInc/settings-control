export class ModuleModel {
    constructor(name, url, buildModifyTime, srcModifyTime, isBuilt, isCloned,
                index = undefined, configPath = undefined, executeName = undefined, detail = false) {
        this.name = name;
        this.url = url;
        this.buildModifyTime = new Date(buildModifyTime);
        this.srcModifyTime = new Date(srcModifyTime);
        this.isBuilt = isBuilt;
        this.isCloned = isCloned;
        this.index = index;
        this.configPath = configPath;
        this.executeName = executeName;
        this.detail = detail;
    }
}

/*
"config_path":"coefficients.json", (core)
"execute":"a.out", (core)
"name":"amv_server",
"build_modify_time":"Thu, 14 Feb 2019 12:41:48 GMT",
"index":1, (dependency)
"is_built":true,
"is_cloned":true,
"src_modify_time":"Thu, 14 Feb 2019 12:41:45 GMT",
"url":"git@bitbucket.org:FOProject/fomodel"
 */
