# MCP Server - Enhanced Outlook Email Integration

This Starlette-based application powers the enhanced MCP server for OutlookAgent. It integrates with Microsoft Graph to provide comprehensive email management capabilities and exposes JSON-RPC compatible endpoints for consumption by Claude and other MCP clients.

---

## 🧰 Enhanced App Flow

1. `main.py` starts the server via `create_starlette_app()`
2. Enhanced Starlette app includes:
   * `Route /sse` for Server-Sent Events transport
   * `Route /health` for availability check
   * `Route /tools` and `/tool_call` for enhanced MCP tool discovery and usage
   * `Route /api/send-email`, `/api/fetch-emails`, `/api/reply-email`, and `/api/forward-email` for comprehensive REST API access
   * Enhanced tool logic registered using `FastMCP` with comprehensive documentation

---

## 🚀 Enhanced Authentication Flow

* **Location**: `services/auth/graph_auth.py`
* **Method**: MSAL Device Code Flow for personal Microsoft accounts
* **Caching**: Token cached in `services/auth/.token.json`
* **Integration**: Token automatically injected into `httpx` calls to Microsoft Graph
* **Validation**: Startup validation with comprehensive error handling
* **Management**: Manual login/logout tools available

---

## 🧱 Enhanced Registered Tools

Located in `server/mcp_email_server.py` with comprehensive documentation:

### **Authentication Tools**
* **`login_tool()`** - Prompts for MSAL device login with enhanced error handling
* **`logout_tool()`** - Clear saved Outlook access token with confirmation

### **Enhanced Email Tools**
* **`send_email_tool()`** - **🚀 ENHANCED** - Advanced email sending with:
  * ✅ Multiple recipients (comma/semicolon separated)
  * ✅ CC and BCC support
  * ✅ Individual vs group delivery modes
  * ✅ HTML and plain text content support
  * ✅ Comprehensive email validation
  * ✅ Detailed error handling and status reporting

* **`fetch_email_tool()`** - Enhanced email retrieval with:
  * ✅ Advanced filtering options
  * ✅ Natural language subject search
  * ✅ Email ID extraction for replies

* **`reply_email_tool()`** - Reply to specific emails using email IDs with:
  * ✅ Email ID-based reply targeting  
  * ✅ Comprehensive error handling
  * ✅ Confirmation of reply status

* **`delete_email_tool()`** - Delete specific emails using email IDs with:
  * ✅ Email ID-based deletion
  * ✅ Comprehensive error handling
  * ✅ Confirmation of deletion status

* **`forward_email_tool()`** - **🚀 NEW** - Forward emails to specific recipients with:
  * ✅ Single recipient forwarding with TO, CC, and BCC support
  * ✅ Automatic "Fw: " prefix addition to subject line
  * ✅ Additional message support before forwarded content
  * ✅ Original email content and formatting preservation
  * ✅ Text and HTML content type support

All tools are auto-discovered by Claude via enhanced `/tools` route and executed via `/tool_call`.

---

## 🌐 Enhanced API Endpoints

### **MCP Protocol Endpoints**
* **`GET /tools`** - Returns enhanced JSON-RPC tool list with comprehensive schemas
* **`POST /tool_call`** - Executes tools with enhanced argument validation and error handling

### **Health & Monitoring**
* **`GET /health`** - Returns `{ "status": "ok" }` with system health information

### **Transport Layer**
* **`GET /sse`** - Establishes event stream connection for real-time communication

### **REST API Endpoints**
* **`POST /api/send-email`** - Enhanced email sending via REST with full feature support
* **`GET /api/fetch-emails`** - Enhanced email fetching via REST with filtering
* **`POST /api/reply-email`** - Reply to specific emails via REST using email IDs
* **`POST /api/forward-email`** - Forward emails to recipients via REST with CC/BCC support

---

## 📚 Enhanced Configuration

`.env` file under `mcp_server/` should include:

```env
# Microsoft Graph / Outlook API
OUTLOOK_CLIENT_ID=your-client-id
OUTLOOK_TENANT_ID=consumers  # or your actual tenant ID
OUTLOOK_SCOPES=User.Read Mail.Read Mail.Send Mail.ReadWrite

# Microsoft Graph API URL
GRAPH_API_URL=https://graph.microsoft.com/v1.0

# Server Configuration
PORT=8000
DEBUG=true

STARLETTE_HOST=127.0.0.1
STARLETTE_PORT=8000
MCP_HOST=127.0.0.1
MCP_PORT=8081
```

---

## 🛠️ Enhanced Tool Architecture

### **MCP Protocol Integration**
* **Enhanced Starlette routes** respond with JSON-RPC 2.0 compliant structure
* **Dynamic tool discovery** - Tools properly exposed in Claude's MCP interface
* **Comprehensive schemas** - All tools include detailed input/output schemas
* **Enhanced proxy script** (`proxy_claude_stdio.py`) with improved error handling

### **Email Processing Pipeline**
* **Input normalization** - `utils/input_utils.py` handles comma/semicolon separation
* **Email validation** - `utils/validators.py` provides comprehensive format validation
* **Payload construction** - `utils/email/email_utils.py` builds Graph API payloads
* **Enhanced error handling** - Per-recipient status tracking and detailed error reporting

### **Utility Modules**
* **`utils/input_utils.py`** - Input normalization for flexible email list formats
* **`utils/validators.py`** - Email format validation with regex patterns
* **`utils/email/email_utils.py`** - Microsoft Graph API payload construction
* **`utils/template_utils.py`** - Template processing utilities

---

## 🔧 Enhanced Dependencies

### **Core Framework**
* **`Starlette`** - Lightweight ASGI framework for HTTP server
* **`httpx`** - Async HTTP client for Microsoft Graph API requests
* **`uvicorn`** - ASGI server with hot reload for development

### **Authentication & Security**
* **`msal`** - Microsoft Authentication Library for OAuth 2.0
* **Enhanced token management** - Secure caching and validation

### **MCP Integration**
* **`FastMCP`** - Enhanced tool registration wrapper with schema support
* **Enhanced proxy communication** - Improved stdio handling for Claude integration

### **Email Processing**
* **Enhanced validation** - Comprehensive email format checking
* **Flexible input handling** - Support for multiple separator formats
* **Rich content support** - HTML and plain text email formatting

---

## 🎯 Recent Enhancements

### **Email Functionality**
- **Multiple recipients** with comma or semicolon separation support
- **CC and BCC functionality** for comprehensive email distribution
- **Individual vs group delivery** modes for personalized or broadcast emails
- **HTML content support** for rich email formatting
- **Enhanced error handling** with per-recipient status tracking
- **Email forwarding** with automatic "Fw: " prefix and content preservation
- **Reply functionality** for responding to specific emails using email IDs

### **MCP Integration**
- **Dynamic tool discovery** - Tools now properly visible in Claude's interface
- **Enhanced proxy communication** - Improved stdio handling and error management
- **Comprehensive documentation** - All tools fully documented with examples
- **Better authentication handling** - Robust token management and validation

### **Architecture Improvements**
- **Modular utility system** - Clean separation of concerns
- **Comprehensive type safety** - Full type hints throughout
- **Enhanced error resilience** - Graceful handling of all error scenarios
- **Improved documentation** - All modules and functions properly documented

---

## 🚀 Performance & Reliability

### **Async Operations**
* **Non-blocking email sending** - Async HTTP client for optimal performance
* **Concurrent processing** - Efficient handling of multiple email operations
* **Connection reuse** - Optimized HTTP connections for Graph API calls

### **Error Handling**
* **Comprehensive validation** - Email format validation before API calls
* **Graceful degradation** - Individual email failures don't stop batch operations
* **Detailed error reporting** - Per-operation status tracking and reporting

### **Security**
* **OAuth 2.0 compliance** - Secure authentication with Microsoft Graph
* **Token management** - Secure caching and automatic refresh handling
* **Input validation** - Protection against malformed email addresses and injection attacks
