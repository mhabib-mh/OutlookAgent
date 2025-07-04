# OutlookAgent

OutlookAgent is a comprehensive MCP server implementation designed to interface with Microsoft Outlook through the Microsoft Graph API. It provides advanced email management capabilities with support for multiple recipients, flexible delivery modes, and seamless integration with Claude via the Model Context Protocol (MCP).

---

## 📁 Project Structure

```bash
OutlookAgent/
├── mcp_server/             # Main application server
│   ├── app/                # Starlette app, routes, health checks
│   ├── config/             # Settings and environment configuration
│   ├── devtools/claude/    # Enhanced MCP proxy handler for Claude (stdio)
│   ├── routes/             # API route handlers (email, tools, etc.)
│   ├── server/             # MCP tool registration via FastMCP
│   ├── services/           # Business logic (auth, email, calendar)
│   │   ├── auth/           # Microsoft Graph authentication
│   │   └── email/          # Enhanced email services
│   ├── transports/         # SSE transport implementation
│   ├── utils/              # Utility modules
│   │   ├── email/          # Email payload construction
│   │   ├── input_utils.py  # Input normalization (comma/semicolon support)
│   │   └── validators.py   # Email validation utilities
│   ├── .env                # Environment variables
│   ├── main.py             # Entry point for uvicorn
│   └── README.md           # Detailed server documentation
├── scripts/                # Windows helper scripts
│   ├── start_server.bat    # ✅ Recommended way to start dev server
│   ├── stop_server.bat     # Stop server
│   ├── restart_server.bat  # Restart server
│   └── README.md           # Scripts documentation
└── README.md               # Project overview (this file)
```

---

## ✅ Enhanced Features

### **🚀 Core Functionality**

- **Microsoft Graph API integration** - Send, fetch, reply to and delete emails
- **Device code flow authentication** for personal Microsoft accounts
- **Claude AI integration** using enhanced MCP stdio interface
- **Starlette-based HTTP routing** with health checks and tool endpoints
- **SSE-based message streaming** for real-time communication

### **📧 Advanced Email Capabilities**

- **✅ Multiple recipients support** - TO, CC, BCC with comma/semicolon separation
- **✅ Flexible delivery modes** - Group emails or individual personalized emails
- **✅ Rich content support** - HTML and plain text formatting
- **✅ Comprehensive validation** - Email format validation before sending
- **✅ Detailed error handling** - Per-recipient status tracking
- **✅ Reply functionality** - Reply to specific emails using email IDs
- **✅ Delete functionality** - Delete specific emails using email IDs

### **🔧 Enhanced MCP Integration**

- **✅ Dynamic tool discovery** - Tools properly exposed in Claude's MCP interface
- **✅ Improved proxy handling** - Enhanced stdio communication with Claude
- **✅ Comprehensive documentation** - All tools fully documented with examples
- **✅ Robust error handling** - Graceful handling of authentication and network issues

---

## 📦 Requirements

- **Python 3.11+**
- **Microsoft account** with Outlook mailbox access
- **Azure registered application** (client ID)
- **Poetry** (dependency management)

---

## ▶️ Development

To run the project:

```bash
scripts/start_server.bat
```

This starts the Uvicorn dev server with reload, and auto-authenticates using MSAL (device flow) if needed. Ensure `.env` is present in `mcp_server/`.

---

## 🧠 Enhanced Claude Integration

Claude can interact with this server through the enhanced `proxy_claude_stdio.py` bridge, enabling comprehensive tool invocation via JSON-RPC over stdio with proper tool discovery.

### **Configuration**

Add this to your `claude_desktop_config.json` (update paths to match your system):

```json
{
  "mcpServers": {
    "outlook-email-mcp-server": {
      "command": "C:/Users/[your-user]/Desktop/ai-projects/OutlookAgent/mcp_server/.venv/Scripts/python.exe",
      "args": [
        "C:/Users/[your-user]/Desktop/ai-projects/OutlookAgent/mcp_server/devtools/claude/proxy_claude_stdio.py"
      ],
      "cwd": "C:/Users/[your-user]/Desktop/ai-projects/OutlookAgent/mcp_server",
      "env": {
        "PYTHONPATH": "C:/Users/[your-user]/Desktop/ai-projects/OutlookAgent"
      }
    }
  }
}
```

### **Available Tools**

After setup, Claude will have access to these tools:

1. **`login_tool`** - Authenticate with Microsoft Outlook
2. **`logout_tool`** - Clear saved access token
3. **`send_email_tool`** - Enhanced email sending with multiple recipients, CC/BCC
4. **`fetch_email_tool`** - Retrieve emails with advanced filtering
5. **`reply_email_tool`** - Reply to specific emails using email IDs
6. **`delete_email_tool`** - Delete specific emails using email IDs

---

## 🎯 Recent Enhancements

### **Email Functionality**

- **Multiple recipients** with comma or semicolon separation
- **CC and BCC support** for comprehensive email distribution
- **Individual vs group delivery** modes for personalized or broadcast emails
- **HTML content support** for rich email formatting
- **Enhanced error handling** with per-recipient status tracking

### **MCP Integration**

- **Dynamic tool discovery** - Tools now properly visible in Claude's interface
- **Enhanced proxy communication** - Improved stdio handling and error management
- **Comprehensive documentation** - All tools fully documented with examples
- **Better authentication handling** - Robust token management and validation

### **Code Quality**

- **Modular architecture** - Clean separation of concerns with utility modules
- **Comprehensive documentation** - All modules and functions properly documented
- **Type safety** - Full type hints and validation throughout
- **Error resilience** - Graceful handling of all error scenarios

---

## 📚 Documentation

- **[Server Documentation](mcp_server/README.md)** - Detailed server architecture and API
- **[Scripts Documentation](scripts/README.md)** - Development helper scripts
- **[Authentication Guide](mcp_server/services/auth/graph_auth.py)** - OAuth 2.0 setup and usage
- **[Email Services](mcp_server/services/email/)** - Email functionality documentation
