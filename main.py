"""
Main entry point for Agentic RAG POC
Provides CLI interface for querying the RAG system.
Compatible with Windows, macOS, and Linux.
"""
import argparse
import logging
import sys
from pathlib import Path

# Add project root to path (cross-platform compatible)
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

from src.rag_system.crew import RAGCrewManager, run_query

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def interactive_mode():
    """Run the RAG system in interactive mode"""
    print("\n" + "="*60)
    print("🤖 Agentic RAG - Interactive Mode")
    print("="*60)
    print("Ask questions about your documents. Type 'quit' to exit.")
    print("Type 'simple' to switch to simple mode, 'full' for full mode.")
    print("="*60 + "\n")
    
    manager = RAGCrewManager(use_simple_mode=False)
    
    while True:
        try:
            query = input("\n📝 Your question: ").strip()
            
            if not query:
                continue
            
            if query.lower() == 'quit':
                print("\n👋 Goodbye!")
                break
            
            if query.lower() == 'simple':
                manager.use_simple_mode = True
                print("✅ Switched to simple (single-agent) mode")
                continue
            
            if query.lower() == 'full':
                manager.use_simple_mode = False
                print("✅ Switched to full (multi-agent) mode")
                continue
            
            print("\n🔍 Searching documents...\n")
            
            result = manager.query(query)
            
            if result.get("success"):
                print("\n" + "="*60)
                print("📄 ANSWER:")
                print("="*60)
                print(result["answer"])
                
                if result.get("sources"):
                    print("\n📚 Sources:", ", ".join(result["sources"]))
            else:
                print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\n❌ Error: {e}")


def single_query_mode(query: str, simple: bool = False):
    """Run a single query and exit"""
    print(f"\n🔍 Processing query: {query}\n")
    
    manager = RAGCrewManager(use_simple_mode=simple)
    result = manager.query(query)
    
    if result.get("success"):
        print("="*60)
        print("📄 ANSWER:")
        print("="*60)
        print(result["answer"])
        
        if result.get("sources"):
            print("\n📚 Sources:", ", ".join(result["sources"]))
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Agentic RAG - Query your documents with AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Interactive mode
  %(prog)s "What are the HR policies?"  # Single query
  %(prog)s --simple "Quick question"    # Simple mode (single agent)
  %(prog)s --server                     # Start API server
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Question to ask (if not provided, enters interactive mode)"
    )
    
    parser.add_argument(
        "--simple", "-s",
        action="store_true",
        help="Use simple single-agent mode"
    )
    
    parser.add_argument(
        "--server",
        action="store_true",
        help="Start the API server instead of CLI"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="API server host (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API server port (default: 8000)"
    )
    
    args = parser.parse_args()
    
    if args.server:
        # Start API server
        from api import run_server
        print(f"🚀 Starting API server at http://{args.host}:{args.port}")
        run_server(host=args.host, port=args.port)
    
    elif args.query:
        # Single query mode
        single_query_mode(args.query, simple=args.simple)
    
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
