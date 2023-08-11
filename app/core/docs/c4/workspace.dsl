/*

HINT use the structurizr VScode extention

 * This is a combined version of the following workspaces:
 *
 * - "Big Bank plc - System Landscape" (https://structurizr.com/share/28201/)
 * - "Big Bank plc - Internet Banking System" (https://structurizr.com/share/36141/)
*/

workspace "Big Bank plc" "This is an example workspace to illustrate the key features of Structurizr, via the DSL, based around a fictional online banking system." {

    model {
        customer = person "Customer" "A customer of Kieback&Peter, with authority over installation(s)." "Customer"

        enterprise "Kieback & Peter | NL" {
            sales_staff = person "Sales Staff" "Handles new customers" "Bank Staff" {
                properties {
                    "Location" "Customer Services"
                }
            }
            service_staff = person "Service Staff" "Deliver service_system" "Bank Staff" {
                properties {
                    "Location" "Internal Services"
                }
            }

            mainframe = softwaresystem "Mainframe KP" "Stores all of the core information about customers, accounts, transactions, etc." "Existing System"
            service_system = softwaresystem "Service System" "Distributes and act on (support) requests."
            
            // atm = softwaresystem "Energy_Provider" "Provider measurements from third party meters." "Existing System"

            web_system = softwaresystem "Webservices" "Gain insights about their installations, request services and ..." {
                properties {
                    "Owner" "Customer Services"
                    "Development Team" "Dev/Internet Services"
                }
                // url https://en.wikipedia.org/wiki/Online_banking

                webapp_container = container "Web Application" "Provides all of the Internet banking functionality to customers via their web browser." "JavaScript and Angular" "Web Browser"
                // mobile_container = container "Mobile App" "Provides a limited subset of the Internet banking functionality to customers via their mobile device." "Xamarin" "Mobile App"
                webpage_container = container "Static Webpage" "Delivers the static content and the Internet banking single page application." "Java and Spring MVC"
                api_container = container "API Application" "Provides Internet banking functionality via a JSON/HTTPS API." "Java and Spring MVC" {
                    signinController = component "Sign In Controller" "Allows users to sign in to the Internet Banking System." "Spring MVC Rest Controller"
                    accountsSummaryController = component "Accounts Summary Controller" "Provides customers with a summary of their bank accounts." "Spring MVC Rest Controller"
                    resetPasswordController = component "Reset Password Controller" "Allows users to reset their passwords with a single use URL." "Spring MVC Rest Controller"
                    securityComponent = component "Security Component" "Provides functionality related to signing in, changing passwords, etc." "Spring Bean"
                    mainframeBankingSystemFacade = component "Mainframe Banking System Facade" "A facade onto the mainframe banking system." "Spring Bean"
                    service_component = component "Service Component" "Sends services to users." "Spring Bean"
                }
                worker_container = container "Worker" "Offload the work of fetching and writing measurements"
                database = container "Database" "Stores user registration information, hashed authentication credentials, access logs, etc." "Oracle Database Schema" "Database"
            }
        }
        energy_provider = softwaresystem "Energy Provider" "Facilitates energy measurements (water, gas, electra) from a third party"


        # relationships between people and software systems
        customer -> web_system "View installation services, invoices and request service"
        web_system -> mainframe "Send billable subscribtions"
        web_system -> service_system "Request service system using"
        service_system -> service_staff "Sends services to"
        service_staff -> customer "Deliver service system to"
        customer -> sales_staff "Requests demo "
        sales_staff -> mainframe "Create demo account"
        // customer -> atm "Withdraws cash using"
        // atm -> mainframe "Uses"
        service_staff -> mainframe "Uses"


        api_container -> worker_container "Request data fetching"
        worker_container -> database "Write data"
        worker_container -> energy_provider "Fetch data"

        # relationships to/from containers
        customer -> webpage_container "Visits bigbank.com/ib using" "HTTPS"
        customer -> webapp_container "Views account balances, and makes payments using"
        // customer -> mobile_container "Views account balances, and makes payments using"
        webpage_container -> webapp_container "Delivers to the customer's web browser"

        # relationships to/from components
        webapp_container -> signinController "Makes API calls to" "JSON/HTTPS"
        webapp_container -> accountsSummaryController "Makes API calls to" "JSON/HTTPS"
        webapp_container -> resetPasswordController "Makes API calls to" "JSON/HTTPS"
        // mobile_container -> signinController "Makes API calls to" "JSON/HTTPS"
        // mobile_container -> accountsSummaryController "Makes API calls to" "JSON/HTTPS"
        // mobile_container -> resetPasswordController "Makes API calls to" "JSON/HTTPS"
        signinController -> securityComponent "Uses"
        accountsSummaryController -> mainframeBankingSystemFacade "Uses"
        resetPasswordController -> securityComponent "Uses"
        resetPasswordController -> service_component "Uses"
        securityComponent -> database "Reads from and writes to" "JDBC"
        mainframeBankingSystemFacade -> mainframe "Makes API calls to" "XML/HTTPS"
        service_component -> service_system "Sends service_system using"

        deploymentEnvironment "Development" {
            deploymentNode "Developer Laptop" "" "Microsoft Windows 10 or Apple macOS" {
                deploymentNode "Web Browser" "" "Chrome, Firefox, Safari, or Edge" {
                    developerwebapp_containerInstance = containerInstance webapp_container
                }
                deploymentNode "Docker Container - Web Server" "" "Docker" {
                    deploymentNode "Apache Tomcat" "" "Apache Tomcat 8.x" {
                        developerwebpage_containerInstance = containerInstance webpage_container
                        developerapi_containerInstance = containerInstance api_container
                    }
                }
                deploymentNode "Docker Container - Database Server" "" "Docker" {
                    deploymentNode "Database Server" "" "Oracle 12c" {
                        developerDatabaseInstance = containerInstance database
                    }
                }
            }
            deploymentNode "Big Bank plc" "" "Big Bank plc data center" "" {
                deploymentNode "bigbank-dev001" "" "" "" {
                    softwareSystemInstance mainframe
                }
            }

        }

        deploymentEnvironment "Live" {
            // deploymentNode "Customer's mobile device" "" "Apple iOS or Android" {
                // livemobile_containerInstance = containerInstance mobile_container
            // }
            deploymentNode "Customer's computer" "" "Microsoft Windows or Apple macOS" {
                deploymentNode "Web Browser" "" "Chrome, Firefox, Safari, or Edge" {
                    livewebapp_containerInstance = containerInstance webapp_container
                }
            }

            deploymentNode "Big Bank plc" "" "Big Bank plc data center" {
                deploymentNode "bigbank-web***" "" "Ubuntu 16.04 LTS" "" 4 {
                    deploymentNode "Apache Tomcat" "" "Apache Tomcat 8.x" {
                        livewebpage_containerInstance = containerInstance webpage_container
                    }
                }
                deploymentNode "bigbank-api***" "" "Ubuntu 16.04 LTS" "" 8 {
                    deploymentNode "Apache Tomcat" "" "Apache Tomcat 8.x" {
                        liveapi_containerInstance = containerInstance api_container
                    }
                }

                deploymentNode "bigbank-db01" "" "Ubuntu 16.04 LTS" {
                    primaryDatabaseServer = deploymentNode "Oracle - Primary" "" "Oracle 12c" {
                        livePrimaryDatabaseInstance = containerInstance database
                    }
                }
                deploymentNode "bigbank-db02" "" "Ubuntu 16.04 LTS" "Failover" {
                    secondaryDatabaseServer = deploymentNode "Oracle - Secondary" "" "Oracle 12c" "Failover" {
                        liveSecondaryDatabaseInstance = containerInstance database "Failover"
                    }
                }
                deploymentNode "bigbank-prod001" "" "" "" {
                    softwareSystemInstance mainframe
                }
            }

            primaryDatabaseServer -> secondaryDatabaseServer "Replicates data to"
        }
    }

    views {
        properties {
            "c4plantuml.elementProperties" "true"
            "generatr.style.colors.primary" "#485fc7"
            "generatr.style.colors.secondary" "#ffffff"
            "generatr.style.faviconPath" "site/favicon.ico"
            "generatr.style.logoPath" "site/logo.png"

            // full list of available "generatr.markdown.flexmark.extensions"
            // "Abbreviation,Admonition,AnchorLink,Aside,Attributes,Autolink,Definition,Emoji,EnumeratedReference,Footnotes,GfmIssues,GfmStrikethroughSubscript,GfmTaskList,GfmUsers,GitLab,Ins,Macros,MediaTags,ResizableImage,Superscript,Tables,TableOfContents,SimulatedTableOfContents,Typographic,WikiLinks,XWikiMacro,YAMLFrontMatter,YouTubeLink"
            // see https://github.com/vsch/flexmark-java/wiki/Extensions
            // ATTENTION:
            // * "generatr.markdown.flexmark.extensions" values must be separated by comma
            // * it's not possible to use "GitLab" and "ResizableImage" extensions together
            // default behaviour, if no generatr.markdown.flexmark.extensions property is specified, is to load the Tables extension only
            "generatr.markdown.flexmark.extensions" "Abbreviation,Admonition,AnchorLink,Attributes,Autolink,Definition,Emoji,Footnotes,GfmTaskList,GitLab,MediaTags,Tables,TableOfContents,Typographic"
        }

        systemlandscape "SystemLandscape" {
            include *
            autoLayout
        }

        systemcontext web_system "SystemContext" {
            include *
            animation {
                web_system
                customer
                mainframe
                service_system
            }
            autoLayout
        }

        container web_system "Containers" {
            include *
            animation {
                customer mainframe service_system
                webpage_container
                webapp_container
                // mobile_container
                api_container
                database
            }
            autoLayout
        }

        component api_container "Components" {
            include *
            animation {
                webapp_container 
                // mobile_container 
                database service_system mainframe
                signinController securityComponent
                accountsSummaryController mainframeBankingSystemFacade
                resetPasswordController service_component
            }
            autoLayout
        }

        dynamic api_container "SignIn" "Summarises how the sign in feature works in the single-page application." {
            webapp_container -> signinController "Submits credentials to"
            signinController -> securityComponent "Validates credentials using"
            securityComponent -> database "select * from users where username = ?"
            database -> securityComponent "Returns user data to"
            securityComponent -> signinController "Returns true if the hashed password matches"
            signinController -> webapp_container "Sends back an authentication token to"
            autoLayout
        }

        deployment web_system "Development" "DevelopmentDeployment" {
            include *
            animation {
                developerwebapp_containerInstance
                developerwebpage_containerInstance developerapi_containerInstance
                developerDatabaseInstance
            }
            autoLayout
        }

        deployment web_system "Live" "LiveDeployment" {
            include *
            animation {
                livewebapp_containerInstance
                // livemobile_containerInstance
                livewebpage_containerInstance liveapi_containerInstance
                livePrimaryDatabaseInstance
                liveSecondaryDatabaseInstance
            }
            autoLayout
        }

        styles {
            element "Person" {
                color #ffffff
                fontSize 22
                shape Person
            }
            element "Customer" {
                background #08427b
            }
            element "Bank Staff" {
                background #999999
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Existing System" {
                background #999999
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Web Browser" {
                shape WebBrowser
            }
            element "Mobile App" {
                shape MobileDeviceLandscape
            }
            element "Database" {
                shape Cylinder
            }
            element "Component" {
                background #85bbf0
                color #000000
            }
            element "Failover" {
                opacity 25
            }
        }
    }
}