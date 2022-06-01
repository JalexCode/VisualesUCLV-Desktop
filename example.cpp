#include <QApplication>
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QStandardItemModel>
#include <QTreeView>
#include <QFileIconProvider>

QStandardItem * findChilItem(QStandardItem *it, const QString & text){
    if(!it->hasChildren())
        return nullptr;
    for(int i=0; i< it->rowCount(); i++){
        if(it->child(i)->text() == text)
            return it->child(i);
    }
    return nullptr;
}

static void appendToModel(QStandardItemModel *model, const QStringList & list, const QString & size){
    QStandardItem *parent = model->invisibleRootItem();
    QFileIconProvider provider;

    for(QStringList::const_iterator it = list.begin(); it != list.end(); ++it)
    {
        QStandardItem *item = findChilItem(parent, *it);
        if(item){
            parent = item;
            continue;
        }
        item = new QStandardItem(*it);
        if(std::next(it) == list.end()){
            item->setIcon(provider.icon(QFileIconProvider::File));
            parent->appendRow({item, new QStandardItem(size)});
        }
        else{
            item->setIcon(provider.icon(QFileIconProvider::Folder));
            parent->appendRow(item);
        }
        parent = item;
    }
}

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QStandardItemModel model;
    model.setHorizontalHeaderLabels({"Name", "Size"});
    const std::string json = R"([
                             {"name":"/folder1/file1.txt";"size":"1KB"},
                             {"name":"/folder1/file2.txt";"size":"1KB"},
                             {"name":"/folder1/sub/file3.txt";"size":"1KB"},
                             {"name":"/folder2/file4.txt";"size":"1KB"},
                             {"name":"/folder2/file5.txt";"size":"1KB"}
                             ])";

    QJsonParseError parse;
    // The string is not a valid json, the separator must be a comma
    // and not a semicolon, which is why it is being replaced
    QByteArray data = QByteArray::fromStdString(json).replace(";", ",");
    QJsonDocument const& jdoc =  QJsonDocument::fromJson(data, &parse);
    Q_ASSERT(parse.error == QJsonParseError::NoError);
    if(jdoc.isArray()){
        for(const QJsonValue &element : jdoc.array() ){
            QJsonObject obj = element.toObject();
            QString name = obj["name"].toString();
            QString size = obj["size"].toString();
            appendToModel(&model, name.split("/", QString::SkipEmptyParts), size);
        }
    }

    QTreeView view;
    view.setModel(&model);
    view.show();
    return a.exec();
}