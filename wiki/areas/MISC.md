# locales/ assets/ contributors/ — auxiliary content

Auxiliary content: `locales/` (i18n YAML), `assets/` (banner art), `contributors/` (credit records), `sustainability/`, eval data dirs.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `.coderabbit.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.dockerignore` | asset | File `.dockerignore` | Repository content; see related files / area page for the enclosing subsystem |  |
| `.envrc` | asset | File `.envrc` | Repository content; see related files / area page for the enclosing subsystem |  |
| `.gitattributes` | asset | File `.gitattributes` | Repository content; see related files / area page for the enclosing subsystem |  |
| `.githooks/pre-commit` | script | Pre-commit coherence guard — stale-doctrine scan + coherence fail-close + dirty-warn | Makes stale doctrine and coherence contradictions impossible to merge | 3v0/core/coherence.py;3v0/scripts/verify.sh;wiki refresh steps |
| `.gitignore` | asset | File `.gitignore` | Repository content; see related files / area page for the enclosing subsystem |  |
| `.hadolint.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.mailmap` | asset | File `.mailmap` | Repository content; see related files / area page for the enclosing subsystem |  |
| `.npmrc` | asset | File `.npmrc` | Repository content; see related files / area page for the enclosing subsystem |  |
| `.nvmrc` | asset | File `.nvmrc` | Repository content; see related files / area page for the enclosing subsystem |  |
| `.prettierignore` | asset | File `.prettierignore` | Repository content; see related files / area page for the enclosing subsystem |  |
| `.prettierrc` | asset | File `.prettierrc` | Repository content; see related files / area page for the enclosing subsystem |  |
| `.python-version` | asset | File `.python-version` | Repository content; see related files / area page for the enclosing subsystem |  |
| `CONTRIBUTING.es.md` | policy-doc | CONTRIBUTING.es policy | Defines the contribution/security contract |  |
| `README.es.md` | readme | Spanish project README | Spanish community surface | README.md;locales/es.yaml |
| `README.ur-pk.md` | readme | README (ur-pk) | Project introduction & quickstart for humans/new agents |  |
| `README.zh-CN.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `SECURITY.es.md` | policy-doc | SECURITY.es policy | Defines the contribution/security contract |  |
| `acp_adapter/__init__.py` | source | ACP (Agent Communication Protocol) adapter for hermes-agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/__main__.py` | source | Allow running the ACP adapter as ``python -m acp_adapter``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/auth.py` | source | ACP auth helpers — detect and advertise Hermes authentication methods. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/edit_approval.py` | source | Pre-execution ACP edit approval helpers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/entry.py` | source | CLI entry point for the hermes-agent ACP adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/events.py` | source | Callback factories for bridging AIAgent events to ACP notifications. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/permissions.py` | source | ACP permission bridging for Hermes dangerous-command approvals. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/provenance.py` | source | Derive ACP session-provenance metadata from the existing compression chain. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/server.py` | source | ACP agent server — exposes Hermes Agent via the Agent Client Protocol. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/session.py` | source | ACP session manager — maps ACP sessions to Hermes AIAgent instances. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `acp_adapter/tools.py` | source | ACP tool-call helpers for mapping hermes tools to ACP ToolKind and building content. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `assets/banner.png` | data | Banner artwork for CLI startup | Branding | ev0_cli/banner.py |
| `cli-config.yaml.example` | asset | File `cli-config.yaml.example` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `contributors/emails/.gitkeep` | asset | File `.gitkeep` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/0301chris@gmail.com` | asset | File `0301chris@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/0xarkstar@users.noreply.github.com` | asset | File `0xarkstar@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/0xprincess@nuconstruct.xyz` | asset | File `0xprincess@nuconstruct.xyz` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/1051445024@qq.com` | asset | File `1051445024@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/114367649+knoal@users.noreply.github.com` | asset | File `114367649+knoal@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/116476090+JeffStone69@users.noreply.github.com` | asset | File `116476090+JeffStone69@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/1265291278@qq.com` | asset | File `1265291278@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/1347825413@qq.com` | asset | File `1347825413@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/1373636680@qq.com` | asset | File `1373636680@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/15167896+2001Y@users.noreply.github.com` | asset | File `15167896+2001Y@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/155588579+spiky02plateau@users.noreply.github.com` | asset | File `155588579+spiky02plateau@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/1759158233@qq.com` | asset | File `1759158233@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/1762459322@qq.com` | asset | File `1762459322@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/1940428933@qq.com` | asset | File `1940428933@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/203146215+monerostar@users.noreply.github.com` | asset | File `203146215+monerostar@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/225291640+camaleonidas@users.noreply.github.com` | asset | File `225291640+camaleonidas@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/232201106@qq.com` | asset | File `232201106@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/2418548+markoub@users.noreply.github.com` | asset | File `2418548+markoub@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/2436887475@qq.com` | asset | File `2436887475@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/260355617@qq.com` | asset | File `260355617@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/262373281+vexclawx31@users.noreply.github.com` | asset | File `262373281+vexclawx31@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/269728612+metamon-p@users.noreply.github.com` | asset | File `269728612+metamon-p@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/275831447+maff-t2b@users.noreply.github.com` | asset | File `275831447+maff-t2b@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/285329547+xaviersudre@users.noreply.github.com` | asset | File `285329547+xaviersudre@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/286182457+Da7-Tech@users.noreply.github.com` | asset | File `286182457+Da7-Tech@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/3115763429@qq.com` | asset | File `3115763429@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/314574126@qq.com` | asset | File `314574126@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/3Nya3@users.noreply.github.com` | asset | File `3Nya3@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/445481611@qq.com` | asset | File `445481611@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/48723787+chuenchen309@users.noreply.github.com` | asset | File `48723787+chuenchen309@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/50810385+tigercraft4@users.noreply.github.com` | asset | File `50810385+tigercraft4@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/55nx954gn6-debug@users.noreply.github.com` | asset | File `55nx954gn6-debug@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/56281588+LevSky22@users.noreply.github.com` | asset | File `56281588+LevSky22@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/602028@ky-tech.com.cn` | asset | File `602028@ky-tech.com.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/604maestro@protonmail.com` | asset | File `604maestro@protonmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/619963502@qq.com` | asset | File `619963502@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/807847218@qq.com` | asset | File `807847218@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/840596168@qq.com` | asset | File `840596168@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/87degrees@87ui-Macmini.local` | asset | File `87degrees@87ui-Macmini.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/Axmr1@users.noreply.github.com` | asset | File `Axmr1@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/Cyrus@ThreeSixs-Mac-Mini.local` | asset | File `Cyrus@ThreeSixs-Mac-Mini.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/DavidMetcalfe@users.noreply.github.com` | asset | File `DavidMetcalfe@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/Enough1122@users.noreply.github.com` | asset | File `Enough1122@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/LauraGPT@users.noreply.github.com` | asset | File `LauraGPT@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/MaxFreedomPollard@users.noreply.github.com` | asset | File `MaxFreedomPollard@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/Nikola@PlayForm.Cloud` | asset | File `Nikola@PlayForm.Cloud` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/Olympus.roots@outlook.com` | asset | File `Olympus.roots@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/Paolo@Dylans-Mac-Studio.local` | asset | File `Paolo@Dylans-Mac-Studio.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/PavelTajdus@users.noreply.github.com` | asset | File `PavelTajdus@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/RichardGuan1@users.noreply.github.com` | asset | File `RichardGuan1@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/RyderFreeman4Logos@gmail.com` | asset | File `RyderFreeman4Logos@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/StanleyStetson@users.noreply.github.com` | asset | File `StanleyStetson@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/Steven.Leath@gmail.com` | asset | File `Steven.Leath@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/TomAce7@users.noreply.github.com` | asset | File `TomAce7@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/Ufonik88@users.noreply.github.com` | asset | File `Ufonik88@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/WojtekMR3@users.noreply.github.com` | asset | File `WojtekMR3@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/XiaoZAZA@users.noreply.github.com` | asset | File `XiaoZAZA@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/YLChen-007@users.noreply.github.com` | asset | File `YLChen-007@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/Zioywishing@users.noreply.github.com` | asset | File `Zioywishing@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ZundamonnoVRChatkaisetu@users.noreply.github.com` | asset | File `ZundamonnoVRChatkaisetu@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/[email protected]` | asset | File `[email protected]` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/a.neyman17@gmail.com` | asset | File `a.neyman17@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/a.weiker@sap.com` | asset | File `a.weiker@sap.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/a9@A9deMac-mini.local` | asset | File `a9@A9deMac-mini.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/a_espinosa@live.com` | asset | File `a_espinosa@live.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/aakash@plasticlabs.ai` | asset | File `aakash@plasticlabs.ai` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/aameobius@gmail.com` | asset | File `aameobius@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/abcdjmm970703@gmail.com` | asset | File `abcdjmm970703@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/abdulsalamalotaibi86@gmail.com` | asset | File `abdulsalamalotaibi86@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/adam@exo.ai` | asset | File `adam@exo.ai` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/admin@diaoan.xyz` | asset | File `admin@diaoan.xyz` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/adrian.soto6@gmail.com` | asset | File `adrian.soto6@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/afgl_mk93@icloud.com` | asset | File `afgl_mk93@icloud.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/afournier@nvidia.com` | asset | File `afournier@nvidia.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/agent@agents-Mac-mini.local` | asset | File `agent@agents-Mac-mini.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/agent@hermes.dev` | asset | File `agent@hermes.dev` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/agent@openclaw.local` | asset | File `agent@openclaw.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/agents@joinsensie.com` | asset | File `agents@joinsensie.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ahamoudhy@gmail.com` | asset | File `ahamoudhy@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ahmedmoro@gmail.com` | asset | File `ahmedmoro@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ahmetsonersancak@anadolu.edu.tr` | asset | File `ahmetsonersancak@anadolu.edu.tr` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ajzrva@gmail.com` | asset | File `ajzrva@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/akitani@akitaninoMac-mini.local` | asset | File `akitani@akitaninoMac-mini.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/akshankrithick305@gmail.com` | asset | File `akshankrithick305@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/akulayash1996@gmail.com` | asset | File `akulayash1996@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/alanrbox@gmail.com` | asset | File `alanrbox@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/alcibiades.eth@protonmail.com` | asset | File `alcibiades.eth@protonmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/aleks.clark@gmail.com` | asset | File `aleks.clark@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/alex-secure@tuta.io` | asset | File `alex-secure@tuta.io` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/alex.moreno161100@gmail.com` | asset | File `alex.moreno161100@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/alexgong7@outlook.com` | asset | File `alexgong7@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/almurat@Almurats-MacBook-Pro.local` | asset | File `almurat@Almurats-MacBook-Pro.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/alvaro.sanchez-mariscal@oracle.com` | asset | File `alvaro.sanchez-mariscal@oracle.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/amdnative@gmail.com` | asset | File `amdnative@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/anatolij.laptev.1991@gmail.com` | asset | File `anatolij.laptev.1991@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/and@appz.cloud` | asset | File `and@appz.cloud` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/andrew.lg.ford@gmail.com` | asset | File `andrew.lg.ford@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/andy@andydeMac-mini-2.local` | asset | File `andy@andydeMac-mini-2.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/angeon922@gmail.com` | asset | File `angeon922@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/anoop.mehendale@gmail.com` | asset | File `anoop.mehendale@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/anthony.ai.assistant@gmail.com` | asset | File `anthony.ai.assistant@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/arccat114@gmail.com` | asset | File `arccat114@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ariel@vortexradar.com` | asset | File `ariel@vortexradar.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/armaandhawan61@gmail.com` | asset | File `armaandhawan61@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/asscan@189.cn` | asset | File `asscan@189.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/assiri@gmail.com` | asset | File `assiri@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/at@aisec.co.il` | asset | File `at@aisec.co.il` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/atakan1705@hotmail.com` | asset | File `atakan1705@hotmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/austinpickett@users.noreply.github.com` | asset | File `austinpickett@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/awain7@gmail.com` | asset | File `awain7@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ayoub@gmail.com` | asset | File `ayoub@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ayushnangia16@gmail.com` | asset | File `ayushnangia16@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/azureuser@Main.n1l05aasmpie5onxhehb5y5gra.lx.internal.cloudapp.net` | asset | File `azureuser@Main.n1l05aasmpie5onxhehb5y5gra.lx.internal.cloudapp.net` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/baslam@users.noreply.github.com` | asset | File `baslam@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/bb@users.noreply.github.com` | asset | File `bb@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/bbasketballer75@gmail.com` | asset | File `bbasketballer75@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/bedirhancode@users.noreply.github.com` | asset | File `bedirhancode@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/beingsabundant@gmail.com` | asset | File `beingsabundant@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ben.ross@moov.io` | asset | File `ben.ross@moov.io` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ben@ben-phillips.net` | asset | File `ben@ben-phillips.net` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ben@whetstone.com.au` | asset | File `ben@whetstone.com.au` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/benjamin-liang@outlook.com` | asset | File `benjamin-liang@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/benjamin2026-dot@users.noreply.github.com` | asset | File `benjamin2026-dot@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/bennybuoy@users.noreply.github.com` | asset | File `bennybuoy@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/bensheridanedwards@gmail.com` | asset | File `bensheridanedwards@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/betodepaola@meta.com` | asset | File `betodepaola@meta.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/biz@topherross.com` | asset | File `biz@topherross.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/borje@dqsverige.se` | asset | File `borje@dqsverige.se` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/bot@bkstock.dev` | asset | File `bot@bkstock.dev` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/boumagent@gmail.com` | asset | File `boumagent@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/brdpedroo@gmail.com` | asset | File `brdpedroo@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/brian717fr@gmail.com` | asset | File `brian717fr@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/brian@bsweatt.com` | asset | File `brian@bsweatt.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/brice@brice.net` | asset | File `brice@brice.net` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/brunopira@gmail.com` | asset | File `brunopira@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/cad@arcabot.ai` | asset | File `cad@arcabot.ai` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/carl@carltaylor.com.au` | asset | File `carl@carltaylor.com.au` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/carl@sempervirens.no` | asset | File `carl@sempervirens.no` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/carlotestor@users.noreply.github.com` | asset | File `carlotestor@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/carnie-bot@openclaw.local` | asset | File `carnie-bot@openclaw.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/carrion256@proton.me` | asset | File `carrion256@proton.me` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/cation98@yahoo.com` | asset | File `cation98@yahoo.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/centerid@naver.com` | asset | File `centerid@naver.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/chancelu@users.noreply.github.com` | asset | File `chancelu@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/chaosxinglong@gmail.com` | asset | File `chaosxinglong@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/checo520@outlook.com` | asset | File `checo520@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/chelsealong@126.com` | asset | File `chelsealong@126.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/chengxizhou6@gmail.com` | asset | File `chengxizhou6@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/chenjin@hermes.local` | asset | File `chenjin@hermes.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/chenyang.yl@alibaba-inc.com` | asset | File `chenyang.yl@alibaba-inc.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/chris@scalelean.com` | asset | File `chris@scalelean.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/cicav@users.noreply.github.com` | asset | File `cicav@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/cjwang@sowork.tw` | asset | File `cjwang@sowork.tw` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ckorhonen@gmail.com` | asset | File `ckorhonen@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/cluster2@Cluster2s-Mac-Studio.local` | asset | File `cluster2@Cluster2s-Mac-Studio.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/cmoiccool@users.noreply.github.com` | asset | File `cmoiccool@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/coder@trevhome.local` | asset | File `coder@trevhome.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/coe0718+tuck@gmail.com` | asset | File `coe0718+tuck@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/coe0718@icloud.com` | asset | File `coe0718@icloud.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/coffee@coffeebot.dev` | asset | File `coffee@coffeebot.dev` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/colin@colingreig.com` | asset | File `colin@colingreig.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/connorjosephblack@gmail.com` | asset | File `connorjosephblack@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/contact@eliebruno.com` | asset | File `contact@eliebruno.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/contact@nytemode.com` | asset | File `contact@nytemode.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/contato@webtecnica.com.br` | asset | File `contato@webtecnica.com.br` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/content@tyfpro.com` | asset | File `content@tyfpro.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/copii.list@gmail.com` | asset | File `copii.list@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/core@lfdm.co` | asset | File `core@lfdm.co` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/craig@shotflame.local` | asset | File `craig@shotflame.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/cto@phrase.local` | asset | File `cto@phrase.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/cursoragent@cursor.com` | asset | File `cursoragent@cursor.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/cwt@users.noreply.github.com` | asset | File `cwt@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/d@rko.rs` | asset | File `d@rko.rs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dai.suzuki.829@gmail.com` | asset | File `dai.suzuki.829@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/damian.kluk.92@gmail.com` | asset | File `damian.kluk.92@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dan.brunsdon@gmail.com` | asset | File `dan.brunsdon@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/daniel.blank@reportsolution.de` | asset | File `daniel.blank@reportsolution.de` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/daniel21436@hotmail.com` | asset | File `daniel21436@hotmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/danielrpike9@gmail.com` | asset | File `danielrpike9@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dasilva.daniel6@gmail.com` | asset | File `dasilva.daniel6@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/david@lexgenius.ai` | asset | File `david@lexgenius.ai` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/deepujain@gmail.com` | asset | File `deepujain@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/degensmoke@gmail.com` | asset | File `degensmoke@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/deusyu@users.noreply.github.com` | asset | File `deusyu@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dev@redeyesolutions.dev` | asset | File `dev@redeyesolutions.dev` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/devops@sycamore.group` | asset | File `devops@sycamore.group` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dhravya@supermemory.com` | asset | File `dhravya@supermemory.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dhruv.raajjeev@gmail.com` | asset | File `dhruv.raajjeev@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dhruvkejri9@gmail.com` | asset | File `dhruvkejri9@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/diamantejc87@gmail.com` | asset | File `diamantejc87@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dickson.neoh@gmail.com` | asset | File `dickson.neoh@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dillontownsel@gmail.com` | asset | File `dillontownsel@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dinmail@gmail.com` | asset | File `dinmail@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dixit.tanmay1995@gmail.com` | asset | File `dixit.tanmay1995@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dnethusahan.h05@gmail.com` | asset | File `dnethusahan.h05@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dombejar@users.noreply.github.com` | asset | File `dombejar@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dominicbejar@gmail.com` | asset | File `dominicbejar@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dongjiang1989@126.com` | asset | File `dongjiang1989@126.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dqdung205@gmail.com` | asset | File `dqdung205@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/drew@kainotomic.com` | asset | File `drew@kainotomic.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/drissman@gmail.com` | asset | File `drissman@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dstkwll@users.noreply.github.com` | asset | File `dstkwll@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/dustin.persek@protonmail.com` | asset | File `dustin.persek@protonmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/eagleyouxiang@gmail.com` | asset | File `eagleyouxiang@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/eapwrk@gmail.com` | asset | File `eapwrk@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/eazye19@users.noreply.github.com` | asset | File `eazye19@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ebablick@hpc-gridware.com` | asset | File `ebablick@hpc-gridware.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/egilewski@egilewski.com` | asset | File `egilewski@egilewski.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/elco@thedaoist.gg` | asset | File `elco@thedaoist.gg` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/elisam@nvidia.com` | asset | File `elisam@nvidia.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ella@cincin.mesh` | asset | File `ella@cincin.mesh` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/eman1369a@gmail.com` | asset | File `eman1369a@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/emilio.jesus.lasheras.romero@nttdata.com` | asset | File `emilio.jesus.lasheras.romero@nttdata.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/emodoteth@gmail.com` | asset | File `emodoteth@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/emopilot@163.com` | asset | File `emopilot@163.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ergorburak33@gmail.com` | asset | File `ergorburak33@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/eri@plasticlabs.ai` | asset | File `eri@plasticlabs.ai` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/esther@feedmob.com` | asset | File `esther@feedmob.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/evangonggyf@gmail.com` | asset | File `evangonggyf@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/executus.ahli@gmail.com` | asset | File `executus.ahli@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ezell.matt@gmail.com` | asset | File `ezell.matt@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/f1aggo_macair@f1aggo-macairdeMacBook-Air.local` | asset | File `f1aggo_macair@f1aggo-macairdeMacBook-Air.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fangliquan@oppo.com` | asset | File `fangliquan@oppo.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fangliquan@qq.com` | asset | File `fangliquan@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fanyu@moonshot.cn` | asset | File `fanyu@moonshot.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fatbigpig979@gmail.com` | asset | File `fatbigpig979@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fazerluga@gmail.com` | asset | File `fazerluga@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fboutboul@free.fr` | asset | File `fboutboul@free.fr` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/felipe.cavalcanti.rj@gmail.com` | asset | File `felipe.cavalcanti.rj@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fengtianyu_danny@163.com` | asset | File `fengtianyu_danny@163.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/floatingrain@yeah.net` | asset | File `floatingrain@yeah.net` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/florianvalade@Florians-Mac-mini.local` | asset | File `florianvalade@Florians-Mac-mini.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fmy3@qq.com` | asset | File `fmy3@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fraser.humphries@gmail.com` | asset | File `fraser.humphries@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fred.vanwagenen@gmail.com` | asset | File `fred.vanwagenen@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/fukutake@convi.ne.jp` | asset | File `fukutake@convi.ne.jp` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/g.atkinson112@gmail.com` | asset | File `g.atkinson112@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gabriel@gabotronics.com` | asset | File `gabriel@gabotronics.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/geoffreybutler94@gmail.com` | asset | File `geoffreybutler94@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gercamjr.dev@gmail.com` | asset | File `gercamjr.dev@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gh.chiller@pm.me` | asset | File `gh.chiller@pm.me` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ghislain.lemeur@gmail.com` | asset | File `ghislain.lemeur@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gigakun@agentmail.to` | asset | File `gigakun@agentmail.to` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gijs@digitalbase.eu` | asset | File `gijs@digitalbase.eu` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/git@gottz.de` | asset | File `git@gottz.de` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/git@hode.co.uk` | asset | File `git@hode.co.uk` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/git@lunarnexus.com` | asset | File `git@lunarnexus.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/github.commits@widow.cc` | asset | File `github.commits@widow.cc` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/github@00b.tech` | asset | File `github@00b.tech` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/githubespresso407@users.noreply.github.com` | asset | File `githubespresso407@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gitong@gmail.com` | asset | File `gitong@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gkd2323c@users.noreply.github.com` | asset | File `gkd2323c@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gkgibeau@gmail.com` | asset | File `gkgibeau@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gnani.nutakki@gmail.com` | asset | File `gnani.nutakki@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gokhansarapevi@gmail.com` | asset | File `gokhansarapevi@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gonzalofrancoceballos@Gonzalos-Mac-mini.local` | asset | File `gonzalofrancoceballos@Gonzalos-Mac-mini.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/greg@border0.com` | asset | File `greg@border0.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/gshall@pm.me` | asset | File `gshall@pm.me` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/guilherme@guilhermeaguiar.com` | asset | File `guilherme@guilhermeaguiar.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/guillaumepeypin@hotmail.fr` | asset | File `guillaumepeypin@hotmail.fr` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/guoyu.li@lcfuturecenter.com` | asset | File `guoyu.li@lcfuturecenter.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/h-chenbin@voyah.com.cn` | asset | File `h-chenbin@voyah.com.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/halaprix@users.noreply.github.com` | asset | File `halaprix@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/halldrix@users.noreply.github.com` | asset | File `halldrix@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/handnew@hotmail.com` | asset | File `handnew@hotmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/handnewb@users.noreply.github.com` | asset | File `handnewb@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hang.li@tcredit.com` | asset | File `hang.li@tcredit.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hanqshih@gmail.com` | asset | File `hanqshih@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hans@groupg.org` | asset | File `hans@groupg.org` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/haowang@HaodeMac-mini.lan` | asset | File `haowang@HaodeMac-mini.lan` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/harp@hermz580.dev` | asset | File `harp@hermz580.dev` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/harrison@medmetricsrx.com` | asset | File `harrison@medmetricsrx.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/harshkamdar67@gmail.com` | asset | File `harshkamdar67@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hbasheer@student.42abudhabi.ae` | asset | File `hbasheer@student.42abudhabi.ae` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hej@romell.se` | asset | File `hej@romell.se` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hello@ianks.com` | asset | File `hello@ianks.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hello@jeromeiveson.com` | asset | File `hello@jeromeiveson.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hello@jpanganiban.com` | asset | File `hello@jpanganiban.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hellofrommorgan@users.noreply.github.com` | asset | File `hellofrommorgan@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/henrino3@gmail.com` | asset | File `henrino3@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hereicq@users.noreply.github.com` | asset | File `hereicq@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hermes-agent@nous.local` | asset | File `hermes-agent@nous.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hermes-agent@nousresearch.com` | asset | File `hermes-agent@nousresearch.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hermes-agent@users.noreply.local` | asset | File `hermes-agent@users.noreply.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hermes@kortify.local` | asset | File `hermes@kortify.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hermes@server.local` | asset | File `hermes@server.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hermesagent424@gmail.com` | asset | File `hermesagent424@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hfsearcy@gmail.com` | asset | File `hfsearcy@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hill.chitsanupong@gmail.com` | asset | File `hill.chitsanupong@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hinablue@gmail.com` | asset | File `hinablue@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hotragn.pettugani_2024@woxsen.edu.in` | asset | File `hotragn.pettugani_2024@woxsen.edu.in` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hubin-ll@foxmail.com` | asset | File `hubin-ll@foxmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hunter.c.yeagley@outlook.com` | asset | File `hunter.c.yeagley@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hunter@mail.com` | asset | File `hunter@mail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/hustwkr@users.noreply.github.com` | asset | File `hustwkr@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/iammotivated@gmail.com` | asset | File `iammotivated@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/idrisalmalki@Idriss-MacBook-Air.local` | asset | File `idrisalmalki@Idriss-MacBook-Air.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ilovethevikings@yahoo.com` | asset | File `ilovethevikings@yahoo.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/info@datachainsystems.com` | asset | File `info@datachainsystems.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/iniak@iniakdeMac-mini.local` | asset | File `iniak@iniakdeMac-mini.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ipkharitonov@gmail.com` | asset | File `ipkharitonov@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/isak@ialogics.com` | asset | File `isak@ialogics.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/isheng-eqi@users.noreply.github.com` | asset | File `isheng-eqi@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/iskysun96@gmail.com` | asset | File `iskysun96@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/israel.lot@gmail.com` | asset | File `israel.lot@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/itzhak.pan@gmail.com` | asset | File `itzhak.pan@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jackoconner55@icloud.com` | asset | File `jackoconner55@icloud.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jake.tracey@noice.net.au` | asset | File `jake.tracey@noice.net.au` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jakub.wolniewicz@gmail.com` | asset | File `jakub.wolniewicz@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/james@terminaloutcomes.com` | asset | File `james@terminaloutcomes.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/janig88@gmail.com` | asset | File `janig88@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jaretbottoms@gmail.com` | asset | File `jaretbottoms@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jasmine@smfworks.com` | asset | File `jasmine@smfworks.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jason@webdevtoday.com` | asset | File `jason@webdevtoday.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jasonfang1993@users.noreply.github.com` | asset | File `jasonfang1993@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jazzwu@163.com` | asset | File `jazzwu@163.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jdgg777@users.noreply.github.com` | asset | File `jdgg777@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jeff.mettel@gmail.com` | asset | File `jeff.mettel@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jeffrey.ying86@live.com` | asset | File `jeffrey.ying86@live.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jerry.ytp@gmail.com` | asset | File `jerry.ytp@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jerry@hermes.local` | asset | File `jerry@hermes.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jesse.casco@gmail.com` | asset | File `jesse.casco@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jethachan@gmail.com` | asset | File `jethachan@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jevin@jevin.org` | asset | File `jevin@jevin.org` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jfduarte09@gmail.com` | asset | File `jfduarte09@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jfmusa2024@gmail.com` | asset | File `jfmusa2024@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jinglun010@gmail.com` | asset | File `jinglun010@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jinshi.zjs@antgroup.com` | asset | File `jinshi.zjs@antgroup.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/joaomarcosdias444@gmail.com` | asset | File `joaomarcosdias444@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jodybagdonas@gmail.com` | asset | File `jodybagdonas@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/joezhang@outlook.com` | asset | File `joezhang@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/johann@Mac.lan` | asset | File `johann@Mac.lan` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/john.kattenhorn.personal@gmail.com` | asset | File `john.kattenhorn.personal@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jonathan@wolftacdigital.com` | asset | File `jonathan@wolftacdigital.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jordan.mymail@gmail.com` | asset | File `jordan.mymail@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jordanh@nvidia.com` | asset | File `jordanh@nvidia.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jordyelfferich15@gmail.com` | asset | File `jordyelfferich15@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jorkeyliu@gmail.com` | asset | File `jorkeyliu@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/joshua@amokk.net` | asset | File `joshua@amokk.net` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jquesnelle@gmail.com` | asset | File `jquesnelle@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jr.razmus@gmail.com` | asset | File `jr.razmus@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jrcrittenden@gmail.com` | asset | File `jrcrittenden@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jrfbch@gmail.com` | asset | File `jrfbch@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jskang@lablup.com` | asset | File `jskang@lablup.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/jun@junho.co` | asset | File `jun@junho.co` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/junhaowanggg@gmail.com` | asset | File `junhaowanggg@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/justin@actual.computer` | asset | File `justin@actual.computer` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/justin@actual.inc` | asset | File `justin@actual.inc` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/justin@bowes.org` | asset | File `justin@bowes.org` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kaiyisg@yahoo.com.sg` | asset | File `kaiyisg@yahoo.com.sg` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kamon@gao-ai.com` | asset | File `kamon@gao-ai.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kascorp@gmail.com` | asset | File `kascorp@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kelsia014@gmail.com` | asset | File `kelsia014@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/keviea@gmail.com` | asset | File `keviea@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kevin@fleetsmarts.net` | asset | File `kevin@fleetsmarts.net` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kevinbanjo@gmail.com` | asset | File `kevinbanjo@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/khanhngoo3116@gmail.com` | asset | File `khanhngoo3116@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kingdomwarrior23@gmail.com` | asset | File `kingdomwarrior23@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kinsonnee@gmail.com` | asset | File `kinsonnee@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/konsisumer@users.noreply.github.com` | asset | File `konsisumer@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kosta963@gmail.com` | asset | File `kosta963@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kray@block.xyz` | asset | File `kray@block.xyz` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kritcha.b+github@dgtpsn.com` | asset | File `kritcha.b+github@dgtpsn.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kshitij@k4poor.dev` | asset | File `kshitij@k4poor.dev` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kshitij@users.noreply.github.com` | asset | File `kshitij@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kshitijkapoor0611@gmail.com` | asset | File `kshitijkapoor0611@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kuangmi@deeparchi.com` | asset | File `kuangmi@deeparchi.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kuangmi@nudge.com.cn` | asset | File `kuangmi@nudge.com.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kubolko@users.noreply.github.com` | asset | File `kubolko@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/kudi3699@gmail.com` | asset | File `kudi3699@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/laithweinberger@gmail.com` | asset | File `laithweinberger@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lamjj622009225@gmail.com` | asset | File `lamjj622009225@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/landaun@gmail.com` | asset | File `landaun@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lanyusea@gmail.com` | asset | File `lanyusea@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/laura@localhost` | asset | File `laura@localhost` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lavinia.beghini@genialcare.com.br` | asset | File `lavinia.beghini@genialcare.com.br` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/leo@gtmcore.ai` | asset | File `leo@gtmcore.ai` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lepetitprince716-prog@users.noreply.github.com` | asset | File `lepetitprince716-prog@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lepetitprince716@gmail.com` | asset | File `lepetitprince716@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lesbetes28@gmail.com` | asset | File `lesbetes28@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lexharddrive69@gmail.com` | asset | File `lexharddrive69@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lg_329@163.com` | asset | File `lg_329@163.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lidangjiang@gmail.com` | asset | File `lidangjiang@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/linhk8@mail2.sysu.edu.cn` | asset | File `linhk8@mail2.sysu.edu.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/linux2011@qq.com` | asset | File `linux2011@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/liqiping@msh.team` | asset | File `liqiping@msh.team` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/liruixinch@outlook.com` | asset | File `liruixinch@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/liyunlong@nemo.video` | asset | File `liyunlong@nemo.video` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lucas.fernandes.df@gmail.com` | asset | File `lucas.fernandes.df@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lucas@policastromd.com` | asset | File `lucas@policastromd.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lucaskvasir@duck.com` | asset | File `lucaskvasir@duck.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/lumina@douno.it` | asset | File `lumina@douno.it` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/luna@hermes.local` | asset | File `luna@hermes.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/luoxiao6645@gmail.com` | asset | File `luoxiao6645@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ly-wang19@users.noreply.github.com` | asset | File `ly-wang19@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/m296064@rohpccpu21.mayo.edu` | asset | File `m296064@rohpccpu21.mayo.edu` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/maartendormenatteysen@hotmail.com` | asset | File `maartendormenatteysen@hotmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/magnus919@pm.me` | asset | File `magnus919@pm.me` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mail.liangyang@gmail.com` | asset | File `mail.liangyang@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/maly.dan@gmail.com` | asset | File `maly.dan@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mannnrachman@users.noreply.github.com` | asset | File `mannnrachman@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/marcolivier@gmail.com` | asset | File `marcolivier@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mariobgsp@gmail.com` | asset | File `mariobgsp@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mariobgsp@users.noreply.github.com` | asset | File `mariobgsp@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/markmnl@fmsg.io` | asset | File `markmnl@fmsg.io` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/markvlcek@gmail.com` | asset | File `markvlcek@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/martin@tinetwork.com` | asset | File `martin@tinetwork.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/marzukia@users.noreply.github.com` | asset | File `marzukia@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mason@masontanguay.com` | asset | File `mason@masontanguay.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/materemias@gmail.com` | asset | File `materemias@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/matt.strawbridge@lotuscollective.ai` | asset | File `matt.strawbridge@lotuscollective.ai` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mattmiller@comfy.org` | asset | File `mattmiller@comfy.org` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mattshapsss@gmail.com` | asset | File `mattshapsss@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/matvey.sakhnenko03@icloud.com` | asset | File `matvey.sakhnenko03@icloud.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mbrooks@slack-corp.com` | asset | File `mbrooks@slack-corp.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mchermes@edu.dreamcatcher.ai` | asset | File `mchermes@edu.dreamcatcher.ai` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/megusta52@proton.me` | asset | File `megusta52@proton.me` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mehmet.kar@std.yildiz.edu.tr` | asset | File `mehmet.kar@std.yildiz.edu.tr` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mehrzad.karami@gmail.com` | asset | File `mehrzad.karami@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/menglipeng@gmail.com` | asset | File `menglipeng@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/menhguin@users.noreply.github.com` | asset | File `menhguin@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/metamind@kakao.com` | asset | File `metamind@kakao.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/michael@example.com` | asset | File `michael@example.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/michael@smfworks.com` | asset | File `michael@smfworks.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/michaelsam00@yahoo.com` | asset | File `michaelsam00@yahoo.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mihaly.schroth@gmail.com` | asset | File `mihaly.schroth@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mike@mlsmith.net` | asset | File `mike@mlsmith.net` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/miniadmin@skshim-mini.local` | asset | File `miniadmin@skshim-mini.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mjolley9@gmail.com` | asset | File `mjolley9@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mkoduri73@gmail.com` | asset | File `mkoduri73@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/moeadham@gmail.com` | asset | File `moeadham@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mohamed.origami@gmail.com` | asset | File `mohamed.origami@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/moisesvs84@gmail.com` | asset | File `moisesvs84@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mollusk@users.noreply.github.com` | asset | File `mollusk@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/motoblurr@users.noreply.github.com` | asset | File `motoblurr@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mpetrelli@gmail.com` | asset | File `mpetrelli@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mrabsaroka@gmail.com` | asset | File `mrabsaroka@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mrgraphitem@gmail.com` | asset | File `mrgraphitem@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mromano3@ad.engr.wisc.edu` | asset | File `mromano3@ad.engr.wisc.edu` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mrz@mrzlab630.pw` | asset | File `mrz@mrzlab630.pw` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mudreac@gmail.com` | asset | File `mudreac@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/muhammadfurqan0100@gmail.com` | asset | File `muhammadfurqan0100@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mvalentin@valensys.net` | asset | File `mvalentin@valensys.net` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/mycodeisbad@gmail.com` | asset | File `mycodeisbad@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/namredips@gmail.com` | asset | File `namredips@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/naqerl@users.noreply.github.com` | asset | File `naqerl@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nawfal.fardana@dana.id` | asset | File `nawfal.fardana@dana.id` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/necipaksahin056@gmail.com` | asset | File `necipaksahin056@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nformenton@Nicolass-MacBook-Air.local` | asset | File `nformenton@Nicolass-MacBook-Air.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nformenton@gmail.com` | asset | File `nformenton@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nicholas.mariani@hotmail.it` | asset | File `nicholas.mariani@hotmail.it` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nickkarhan@users.noreply.github.com` | asset | File `nickkarhan@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nicochase@users.noreply.github.com` | asset | File `nicochase@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nicolasdmolina76@gmail.com` | asset | File `nicolasdmolina76@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nikita.barkov@jetbrains.com` | asset | File `nikita.barkov@jetbrains.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nkreadly@gmail.com` | asset | File `nkreadly@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nnqbao@gmail.com` | asset | File `nnqbao@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nolanchic@gmail.com` | asset | File `nolanchic@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/noreply@anthropic.com` | asset | File `noreply@anthropic.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/normanking@me.com` | asset | File `normanking@me.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nsovipgl@gmail.com` | asset | File `nsovipgl@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nwadwa@gmail.com` | asset | File `nwadwa@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nyaruko@hermes` | asset | File `nyaruko@hermes` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/nypyouxiang@163.com` | asset | File `nypyouxiang@163.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ohs2251@naver.com` | asset | File `ohs2251@naver.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ojassharma16@gmail.com` | asset | File `ojassharma16@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/okalentiev@gmail.com` | asset | File `okalentiev@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/omid3098@gmail.com` | asset | File `omid3098@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/pa.sen@outlook.com` | asset | File `pa.sen@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/pan.luo@ubc.ca` | asset | File `pan.luo@ubc.ca` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/panding99@outlook.com` | asset | File `panding99@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/pantinor@redhat.com` | asset | File `pantinor@redhat.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/patrickmuller@outlook.com` | asset | File `patrickmuller@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/paul@21million.ad` | asset | File `paul@21million.ad` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/peace@trippyogi.com` | asset | File `peace@trippyogi.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/phixxation@gmail.com` | asset | File `phixxation@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/phm543@gmail.com` | asset | File `phm543@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/phull@phullcutz.de` | asset | File `phull@phullcutz.de` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/pink@macmini-hermes.local` | asset | File `pink@macmini-hermes.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/piyushbag4@gmail.com` | asset | File `piyushbag4@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/pooyan6@gmail.com` | asset | File `pooyan6@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/pouya.ataei.7@gmail.com` | asset | File `pouya.ataei.7@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/praneshnikhar@gmail.com` | asset | File `praneshnikhar@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/professorpalmer9@gmail.com` | asset | File `professorpalmer9@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/prontsevich@gmail.com` | asset | File `prontsevich@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/punyko8@users.noreply.github.com` | asset | File `punyko8@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/qlskssk@gmail.com` | asset | File `qlskssk@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/qlyf@QLYFdeMacBook-Air.local` | asset | File `qlyf@QLYFdeMacBook-Air.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rain@synth.kitchen` | asset | File `rain@synth.kitchen` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/randy@heroictek.com` | asset | File `randy@heroictek.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/razultull@gmail.com` | asset | File `razultull@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/redpiggy-cyber@users.noreply.github.com` | asset | File `redpiggy-cyber@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/reinbeumer@gmail.com` | asset | File `reinbeumer@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/reneisaipa@gmail.com` | asset | File `reneisaipa@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rg@replygirl.club` | asset | File `rg@replygirl.club` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rgerrish@outlook.com` | asset | File `rgerrish@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/richard.ham@live.com` | asset | File `richard.ham@live.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/richard@workflowgroup.com` | asset | File `richard@workflowgroup.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/richardhojunjang@gmail.com` | asset | File `richardhojunjang@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rickard@kumobits.com` | asset | File `rickard@kumobits.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rjhilgefort@gmail.com` | asset | File `rjhilgefort@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rkfshakti@gmail.com` | asset | File `rkfshakti@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rkt.2@hotmail.com` | asset | File `rkt.2@hotmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rmk799@outlook.com` | asset | File `rmk799@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rob@cocodelivery.com` | asset | File `rob@cocodelivery.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rob@zolkos.com` | asset | File `rob@zolkos.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/robbyczgw@gmail.com` | asset | File `robbyczgw@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/robertsryan_21@icloud.com` | asset | File `robertsryan_21@icloud.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rod.boev@gmail.com` | asset | File `rod.boev@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rod@nxtlevel.dev` | asset | File `rod@nxtlevel.dev` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rodrigo@nxtlevelsaas.com` | asset | File `rodrigo@nxtlevelsaas.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/roger.hanhong@gmail.com` | asset | File `roger.hanhong@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rsayar@uvic.ca` | asset | File `rsayar@uvic.ca` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rsherman@velocityinteractive.com` | asset | File `rsherman@velocityinteractive.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rsk-731@users.noreply.github.com` | asset | File `rsk-731@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rt.cms012@gmail.com` | asset | File `rt.cms012@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/rudimar@outlook.com` | asset | File `rudimar@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ruizanthony@users.noreply.github.com` | asset | File `ruizanthony@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ruslan.vasylev.vfx@gmail.com` | asset | File `ruslan.vasylev.vfx@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ryan.kelln@gmail.com` | asset | File `ryan.kelln@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/s0xn1ck@proton.me` | asset | File `s0xn1ck@proton.me` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/s@Ss-MacBook-Pro.local` | asset | File `s@Ss-MacBook-Pro.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/saitama@saitamas-MacBook-Pro.local` | asset | File `saitama@saitamas-MacBook-Pro.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sascha.haase@textiletsg.com` | asset | File `sascha.haase@textiletsg.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/schattenan@kagaku.eu` | asset | File `schattenan@kagaku.eu` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sdevinarayanan@asymbl.com` | asset | File `sdevinarayanan@asymbl.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/seashore.shi@gmail.com` | asset | File `seashore.shi@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sebastian@mause.online` | asset | File `sebastian@mause.online` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sergey@3dacademysoftware.com` | asset | File `sergey@3dacademysoftware.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/seth@rapchat.com` | asset | File `seth@rapchat.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/seze@andrew.cmu.edu` | asset | File `seze@andrew.cmu.edu` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/shag@agentmail.to` | asset | File `shag@agentmail.to` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/shellybotmoyer@users.noreply.github.com` | asset | File `shellybotmoyer@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/shikanga-hermes@shikanga.co.uk` | asset | File `shikanga-hermes@shikanga.co.uk` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/shiqiming.sqm@taobao.com` | asset | File `shiqiming.sqm@taobao.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/shubhambc09@gmail.com` | asset | File `shubhambc09@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/siage@139.com` | asset | File `siage@139.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/simon@everythingmma.com.au` | asset | File `simon@everythingmma.com.au` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/simonmmafs@users.noreply.github.com` | asset | File `simonmmafs@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/simonvanlaak@users.noreply.github.com` | asset | File `simonvanlaak@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sjq15251852316@gmail.com` | asset | File `sjq15251852316@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sjungwon03@gmail.com` | asset | File `sjungwon03@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/skool@doctablade.com` | asset | File `skool@doctablade.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/skywind5487@gmail.com` | asset | File `skywind5487@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/soheil.fakour@gmail.com` | asset | File `soheil.fakour@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/songotenukraine@gmail.com` | asset | File `songotenukraine@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sophia@hermes.local` | asset | File `sophia@hermes.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sora.bluesky.dev@gmail.com` | asset | File `sora.bluesky.dev@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/soundbrokaz@kakao.com` | asset | File `soundbrokaz@kakao.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/spark@channel.inc` | asset | File `spark@channel.inc` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/spfcraze@users.noreply.github.com` | asset | File `spfcraze@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ssahaun19@gmail.com` | asset | File `ssahaun19@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sswdarius@gmail.com` | asset | File `sswdarius@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/stanislav@local` | asset | File `stanislav@local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/stephenlopez2030@gmail.com` | asset | File `stephenlopez2030@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/steve.darlow@gmail.com` | asset | File `steve.darlow@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/stoltemberg@users.noreply.github.com` | asset | File `stoltemberg@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/subhoya@gmail.com` | asset | File `subhoya@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sun.guoen0@gmail.com` | asset | File `sun.guoen0@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/suparious@users.noreply.github.com` | asset | File `suparious@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/support@captureclient.net` | asset | File `support@captureclient.net` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/sylbae@users.noreply.github.com` | asset | File `sylbae@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/szzhoujiarui@users.noreply.github.com` | asset | File `szzhoujiarui@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/takumisatojpn@gmail.com` | asset | File `takumisatojpn@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/tangyi@DESKTOP-2U4MD8Q` | asset | File `tangyi@DESKTOP-2U4MD8Q` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/tars@users.noreply.github.com` | asset | File `tars@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/tbsonline@protonmail.com` | asset | File `tbsonline@protonmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/team@williepeacock.com` | asset | File `team@williepeacock.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/texasich@users.noreply.github.com` | asset | File `texasich@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/the3asic@users.noreply.github.com` | asset | File `the3asic@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/theone139344@users.noreply.github.com` | asset | File `theone139344@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/theunathi@gmail.com` | asset | File `theunathi@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/tikkanadityajyothi@gmail.com` | asset | File `tikkanadityajyothi@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/tobiassafaie@MacBook-Air-von-Tobias-3.local` | asset | File `tobiassafaie@MacBook-Air-von-Tobias-3.local` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/topazd2@gmail.com` | asset | File `topazd2@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/toprakeker@users.noreply.github.com` | asset | File `toprakeker@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/trkim@vms-solutions.com` | asset | File `trkim@vms-solutions.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/tron@chriswykel.com` | asset | File `tron@chriswykel.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/tugrulgunr@gmail.com` | asset | File `tugrulgunr@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/turgut.kural@gmail.com` | asset | File `turgut.kural@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/tusharanshu18@gmail.com` | asset | File `tusharanshu18@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/tutors1997@outlook.com` | asset | File `tutors1997@outlook.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/ulises.millanguerrero@gmail.com` | asset | File `ulises.millanguerrero@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/unashamed366@gmail.com` | asset | File `unashamed366@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/universeszym@mail.ustc.edu.cn` | asset | File `universeszym@mail.ustc.edu.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/unixwzrd.register@mac.com` | asset | File `unixwzrd.register@mac.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/uperLu@users.noreply.github.com` | asset | File `uperLu@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/upicat@users.noreply.github.com` | asset | File `upicat@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/uplink.punks-1k@icloud.com` | asset | File `uplink.punks-1k@icloud.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/vaibhavs362@gmail.com` | asset | File `vaibhavs362@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/valda68k@gmail.com` | asset | File `valda68k@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/vanshgilhotra8885@gmail.com` | asset | File `vanshgilhotra8885@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/venkatbalaji2004@gmail.com` | asset | File `venkatbalaji2004@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/veryverybigdog@gmail.com` | asset | File `veryverybigdog@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/victor@nousresearch.com` | asset | File `victor@nousresearch.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/vikyw89@gmail.com` | asset | File `vikyw89@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/vinoth12940@users.noreply.github.com` | asset | File `vinoth12940@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/viteballoons@gmail.com` | asset | File `viteballoons@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/vitor@vitorcepedalopes.com` | asset | File `vitor@vitorcepedalopes.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/vittoria3103.123@gmail.com` | asset | File `vittoria3103.123@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/voodoo-pixels@Mac.localdomain` | asset | File `voodoo-pixels@Mac.localdomain` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/vovik-assistant@proton.me` | asset | File `vovik-assistant@proton.me` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wangs.coder@gmail.com` | asset | File `wangs.coder@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wangyunyou@leoao.com` | asset | File `wangyunyou@leoao.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wayne1992127@gmail.com` | asset | File `wayne1992127@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/webtecnica@gmail.com` | asset | File `webtecnica@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/webtecnica@users.noreply.github.com` | asset | File `webtecnica@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wen0531@gmail.com` | asset | File `wen0531@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wenzel.james.r@gmail.com` | asset | File `wenzel.james.r@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wernerhp@users.noreply.github.com` | asset | File `wernerhp@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wilgefortz@gmail.com` | asset | File `wilgefortz@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/will@startupbros.com` | asset | File `will@startupbros.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/william.reed@acquia.com` | asset | File `william.reed@acquia.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/williamchastain2005@gmail.com` | asset | File `williamchastain2005@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wrjie@msn.cn` | asset | File `wrjie@msn.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wubu.bounty.hunter@users.noreply.github.com` | asset | File `wubu.bounty.hunter@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/wykim777@naver.com` | asset | File `wykim777@naver.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/xaydinoktay@gmail.com` | asset | File `xaydinoktay@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/xiehong@xinjikang.cn` | asset | File `xiehong@xinjikang.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/xiongyue_hnu@163.com` | asset | File `xiongyue_hnu@163.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/xqdwww@qq.com` | asset | File `xqdwww@qq.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/xrwang8@gmail.com` | asset | File `xrwang8@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/xwlyy1991@163.com` | asset | File `xwlyy1991@163.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/yemi@lagosinternationalmarket.com` | asset | File `yemi@lagosinternationalmarket.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/yflmq001@users.noreply.github.com` | asset | File `yflmq001@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/yingwaizhiying@gmail.com` | asset | File `yingwaizhiying@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/yukinomon@users.noreply.github.com` | asset | File `yukinomon@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/yuntianqing@yahoo.com` | asset | File `yuntianqing@yahoo.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/yuri@sparkroad.com` | asset | File `yuri@sparkroad.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/yuzilong.leif@gmail.com` | asset | File `yuzilong.leif@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/yy28@vip.sina.com` | asset | File `yy28@vip.sina.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/z23@users.noreply.github.com` | asset | File `z23@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zabih.mosafer@gmail.com` | asset | File `zabih.mosafer@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zcj1122@example.com` | asset | File `zcj1122@example.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zehuaw@mit.edu` | asset | File `zehuaw@mit.edu` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zgzczzw@users.noreply.github.com` | asset | File `zgzczzw@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zhangk1985@gmail.com` | asset | File `zhangk1985@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zhjay@stu.xjtu.edu.cn` | asset | File `zhjay@stu.xjtu.edu.cn` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zhouou6@users.noreply.github.com` | asset | File `zhouou6@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zhunyunjiang@gmail.com` | asset | File `zhunyunjiang@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zkgit.substance129@passmail.com` | asset | File `zkgit.substance129@passmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zombopanda@gmail.com` | asset | File `zombopanda@gmail.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/zqw3719222@163.com` | asset | File `zqw3719222@163.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `contributors/emails/{ID}+{username}@users.noreply.github.com` | asset | File `{ID}+{username}@users.noreply.github.com` | Repository content; see related files / area page for the enclosing subsystem |  |
| `datagen-config-examples/example_browser_tasks.jsonl` | asset | File `example_browser_tasks.jsonl` | Repository content; see related files / area page for the enclosing subsystem |  |
| `datagen-config-examples/run_browser_tasks.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `datagen-config-examples/trajectory_compression.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `datagen-config-examples/web_research.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `docker-compose.windows.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `docker-compose.yml` | config | Single-node compose stack | Docker deployment entry | Dockerfile;docker-compose.windows.yml |
| `eslint.config.shared.mjs` | asset | File `eslint.config.shared.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `locales/af.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/ar.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/de.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/en.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/es.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/fr.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/ga.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/hu.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/it.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/ja.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/ko.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/pt.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/ru.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/tr.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/uk.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/zh-hant.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `locales/zh.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `mcp-research-data/ue_bench_rows.json` | data | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `mcp-research-data/ue_bench_summary.json` | data | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `mcp-research-data/ue_discovery_rows.json` | data | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `mcp-research-data/ue_hard_haiku_rows.json` | data | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `mcp-research-data/ue_hard_rows.json` | data | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-mcps/airtable/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/asana/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/atlassian/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/comfy-cloud/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/datadog/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/figma/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/hugging_face/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/intercom/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/linear/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/n8n/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/netlify/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/notion/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/paypal/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/sentry/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/square/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/stripe/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/supabase/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/unreal-engine/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/vercel/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-mcps/webflow/manifest.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `sustainability/fiverr/COMPETITOR_ANALYSIS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/RESEARCH_TOOLING.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/SETUP.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/assets/code-review-sample.pdf` | asset | File `code-review-sample.pdf` | Repository content; see related files / area page for the enclosing subsystem |  |
| `sustainability/fiverr/assets/debug-sample.pdf` | asset | File `debug-sample.pdf` | Repository content; see related files / area page for the enclosing subsystem |  |
| `sustainability/fiverr/assets/gallery-agent-run.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `sustainability/fiverr/assets/gallery-before-after-finding.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `sustainability/fiverr/assets/gallery-root-cause-report.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `sustainability/fiverr/assets/gallery-validation-report.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `sustainability/fiverr/assets/gig-ai-agent.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `sustainability/fiverr/assets/gig-automation.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `sustainability/fiverr/assets/gig-debug.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `sustainability/fiverr/assets/gig-review.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `sustainability/fiverr/assets/gig-scraping.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `sustainability/fiverr/assets/root-cause-report-sample.pdf` | asset | File `root-cause-report-sample.pdf` | Repository content; see related files / area page for the enclosing subsystem |  |
| `sustainability/fiverr/gigs.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/intro-video-script.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/make_gallery.py` | source | Render 4 gallery proof cards for the Fiverr gigs (1280x769, dark premium). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `sustainability/fiverr/make_pdfs.py` | source | Convert the portfolio markdown samples to simple, clean PDFs for the Fiverr gallery. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `sustainability/fiverr/portfolio/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `sustainability/fiverr/portfolio/agent-demo/agent-runbook.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/portfolio/automation-demo/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `sustainability/fiverr/portfolio/automation-demo/clean_orders.py` | source | Clean a weekly orders CSV: dedupe rows, fill blank prices, print a summary. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `sustainability/fiverr/portfolio/automation-demo/sample-orders.csv` | asset | File `sample-orders.csv` | Repository content; see related files / area page for the enclosing subsystem |  |
| `sustainability/fiverr/portfolio/automation-demo/test_clean_orders.py` | test | Python module `test_clean_orders.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `sustainability/fiverr/portfolio/root-cause-report-sample.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/portfolio/scraper-demo/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `sustainability/fiverr/portfolio/scraper-demo/extract_products.py` | source | Extract product cards from an HTML file into CSV, with a validation report. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `sustainability/fiverr/portfolio/scraper-demo/fixtures/products.html` | asset | File `products.html` | Repository content; see related files / area page for the enclosing subsystem |  |
| `sustainability/fiverr/portfolio/scraper-demo/test_extract_products.py` | test | Python module `test_extract_products.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `sustainability/fiverr/profile.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/quick-responses.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/samples/automation-sample.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/samples/code-review-sample.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/fiverr/samples/debug-sample.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `sustainability/wallet.md` | doc | Sustainability wallet ledger | Spend governance | SUSTAINABILITY.md |
| `wiki/README.md` | doc | One-paragraph orientation to the wiki | Fast entry for humans | wiki/index.md |
| `wiki/SCHEMA.md` | doc | The wiki maintenance contract — invariant, artifacts, workflow, failure modes | Defines what must stay true for the index to be trusted | scripts/build_wiki.py;.githooks/pre-commit |
| `wiki/areas/AGENT.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/APPS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/CLI.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/CORE.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/CRON.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/DOCS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/GATEWAY.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/INFRA.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/MISC.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/PLUGINS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/PROVIDERS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/ROOT.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/SCRIPTS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/SKILLS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/STATE.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/TESTS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/TOOLS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/UITUI.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/WEB.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/WEBSITE.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_AGENT.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_APPS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_CLI.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_CORE.md` | doc | Hand-written CORE area narrative, prepended to areas/CORE.md | Human-owned narrative survives regenerated tables | scripts/build_wiki.py |
| `wiki/areas/_intro_CRON.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_DOCS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_GATEWAY.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_INFRA.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_MISC.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_PLUGINS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_PROVIDERS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_ROOT.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_SCRIPTS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_SKILLS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_STATE.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_TESTS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_TOOLS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_UITUI.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_WEB.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/areas/_intro_WEBSITE.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `wiki/curated.tsv` | data | Hand-curated overlay — manual rows merged on --rebuild | Where hand-written entries live (never clobbered); 6 cols/row | scripts/build_wiki.py;wiki/manifest.tsv |
| `wiki/index.md` | doc | Master catalog + reading order for the LLM wiki | The first file an agent reads to map the repo | wiki/SCHEMA.md;wiki/areas/ |
| `wiki/log.md` | doc | Append-only change log for the wiki itself | Audit trail of wiki schema/coverage changes | wiki/SCHEMA.md |
| `wiki/manifest.tsv` | data | Raw 100%-coverage catalog — 6-col TSV rows for every tracked path | The generated artifact --check verifies; commit it | scripts/build_wiki.py;wiki/index.md |
